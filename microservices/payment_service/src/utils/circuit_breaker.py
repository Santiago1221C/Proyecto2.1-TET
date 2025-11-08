"""
Circuit Breaker implementation for Payment Service
Provides fault tolerance and resilience patterns
"""
import time
import logging
from enum import Enum
from typing import Callable, Any, Optional
from functools import wraps
import threading

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, requests fail fast
    HALF_OPEN = "half_open"  # Testing if service is back

class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open"""
    pass

class CircuitBreaker:
    """
    Circuit Breaker implementation with configurable thresholds
    """
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 expected_exception: type = Exception,
                 name: str = "circuit_breaker"):
        """
        Initialize circuit breaker
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time in seconds before trying to close circuit
            expected_exception: Exception type to count as failures
            name: Name for logging purposes
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.name = name
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.lock = threading.Lock()
        
        logger.info(f"Circuit breaker '{name}' initialized with threshold {failure_threshold}")
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: If circuit is open
        """
        with self.lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    logger.info(f"Circuit breaker '{self.name}' moved to HALF_OPEN state")
                else:
                    raise CircuitBreakerError(f"Circuit breaker '{self.name}' is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
            
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful call"""
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                logger.info(f"Circuit breaker '{self.name}' moved to CLOSED state")
            
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit breaker '{self.name}' moved to OPEN state after {self.failure_count} failures")
    
    def get_state(self) -> CircuitState:
        """Get current circuit state"""
        return self.state
    
    def get_metrics(self) -> dict:
        """Get circuit breaker metrics"""
        return {
            'name': self.name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'last_failure_time': self.last_failure_time,
            'failure_threshold': self.failure_threshold,
            'recovery_timeout': self.recovery_timeout
        }

def circuit_breaker(failure_threshold: int = 5, 
                   recovery_timeout: int = 60,
                   expected_exception: type = Exception,
                   name: Optional[str] = None):
    """
    Decorator for circuit breaker functionality
    
    Args:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Time in seconds before trying to close circuit
        expected_exception: Exception type to count as failures
        name: Name for the circuit breaker
    """
    def decorator(func: Callable) -> Callable:
        circuit_name = name or f"{func.__module__}.{func.__name__}"
        breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            expected_exception=expected_exception,
            name=circuit_name
        )
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        # Add circuit breaker instance to wrapper for access
        wrapper.circuit_breaker = breaker
        return wrapper
    
    return decorator

class RetryPolicy:
    """
    Retry policy implementation with exponential backoff
    """
    
    def __init__(self,
                 max_attempts: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True,
                 retryable_exceptions: tuple = (Exception,)):
        """
        Initialize retry policy
        
        Args:
            max_attempts: Maximum number of retry attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
            jitter: Whether to add random jitter
            retryable_exceptions: Tuple of exceptions that should trigger retry
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions
        
        logger.info(f"Retry policy initialized: max_attempts={max_attempts}, base_delay={base_delay}")
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with retry policy
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Last exception if all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
                
            except self.retryable_exceptions as e:
                last_exception = e
                
                if attempt == self.max_attempts - 1:
                    logger.error(f"All {self.max_attempts} attempts failed for {func.__name__}")
                    raise e
                
                delay = self._calculate_delay(attempt)
                logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay:.2f}s")
                time.sleep(delay)
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt"""
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)
        
        if self.jitter:
            import random
            delay *= (0.5 + random.random() * 0.5)  # Add ±25% jitter
        
        return delay

def retry(max_attempts: int = 3,
          base_delay: float = 1.0,
          max_delay: float = 60.0,
          exponential_base: float = 2.0,
          jitter: bool = True,
          retryable_exceptions: tuple = (Exception,)):
    """
    Decorator for retry functionality
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        jitter: Whether to add random jitter
        retryable_exceptions: Tuple of exceptions that should trigger retry
    """
    def decorator(func: Callable) -> Callable:
        policy = RetryPolicy(
            max_attempts=max_attempts,
            base_delay=base_delay,
            max_delay=max_delay,
            exponential_base=exponential_base,
            jitter=jitter,
            retryable_exceptions=retryable_exceptions
        )
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return policy.execute(func, *args, **kwargs)
        
        return wrapper
    
    return decorator

class ResilienceManager:
    """
    Centralized resilience management for the application
    """
    
    def __init__(self):
        self.circuit_breakers = {}
        self.retry_policies = {}
    
    def get_circuit_breaker(self, name: str, **kwargs) -> CircuitBreaker:
        """Get or create circuit breaker"""
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(name=name, **kwargs)
        return self.circuit_breakers[name]
    
    def get_retry_policy(self, name: str, **kwargs) -> RetryPolicy:
        """Get or create retry policy"""
        if name not in self.retry_policies:
            self.retry_policies[name] = RetryPolicy(**kwargs)
        return self.retry_policies[name]
    
    def get_metrics(self) -> dict:
        """Get all resilience metrics"""
        return {
            'circuit_breakers': {
                name: breaker.get_metrics() 
                for name, breaker in self.circuit_breakers.items()
            },
            'retry_policies': {
                name: {
                    'max_attempts': policy.max_attempts,
                    'base_delay': policy.base_delay,
                    'max_delay': policy.max_delay
                }
                for name, policy in self.retry_policies.items()
            }
        }

# Global resilience manager instance
resilience_manager = ResilienceManager()

