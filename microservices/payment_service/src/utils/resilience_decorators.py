"""
Resilience decorators for Payment Service
Combines circuit breaker and retry patterns
"""
import logging
from functools import wraps
from typing import Callable, Any, Optional, Tuple
from .circuit_breaker import circuit_breaker, retry, resilience_manager

logger = logging.getLogger(__name__)

def resilient_service(service_name: str,
                     circuit_breaker_config: Optional[dict] = None,
                     retry_config: Optional[dict] = None):
    """
    Decorator that combines circuit breaker and retry patterns for service calls
    
    Args:
        service_name: Name of the service for circuit breaker identification
        circuit_breaker_config: Configuration for circuit breaker
        retry_config: Configuration for retry policy
    """
    def decorator(func: Callable) -> Callable:
        # Default configurations
        cb_config = circuit_breaker_config or {
            'failure_threshold': 5,
            'recovery_timeout': 60,
            'expected_exception': Exception
        }
        
        retry_config_default = retry_config or {
            'max_attempts': 3,
            'base_delay': 1.0,
            'max_delay': 30.0,
            'exponential_base': 2.0,
            'jitter': True,
            'retryable_exceptions': (Exception,)
        }
        
        # Apply retry decorator first
        retry_decorator = retry(**retry_config_default)
        retry_func = retry_decorator(func)
        
        # Apply circuit breaker decorator
        cb_decorator = circuit_breaker(name=service_name, **cb_config)
        resilient_func = cb_decorator(retry_func)
        
        # Add service name to function for monitoring
        resilient_func.service_name = service_name
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Calling resilient service: {service_name}")
            try:
                return resilient_func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Resilient service {service_name} failed: {str(e)}")
                raise
        
        return wrapper
    
    return decorator

def resilient_database_operation(operation_name: str):
    """
    Decorator for database operations with resilience patterns
    
    Args:
        operation_name: Name of the database operation
    """
    return resilient_service(
        service_name=f"database_{operation_name}",
        circuit_breaker_config={
            'failure_threshold': 3,
            'recovery_timeout': 30,
            'expected_exception': Exception
        },
        retry_config={
            'max_attempts': 3,
            'base_delay': 0.5,
            'max_delay': 10.0,
            'exponential_base': 2.0,
            'jitter': True,
            'retryable_exceptions': (Exception,)
        }
    )

def resilient_external_api(api_name: str):
    """
    Decorator for external API calls with resilience patterns
    
    Args:
        api_name: Name of the external API
    """
    return resilient_service(
        service_name=f"external_api_{api_name}",
        circuit_breaker_config={
            'failure_threshold': 5,
            'recovery_timeout': 60,
            'expected_exception': Exception
        },
        retry_config={
            'max_attempts': 3,
            'base_delay': 1.0,
            'max_delay': 30.0,
            'exponential_base': 2.0,
            'jitter': True,
            'retryable_exceptions': (Exception,)
        }
    )

def resilient_message_queue(queue_name: str):
    """
    Decorator for message queue operations with resilience patterns
    
    Args:
        queue_name: Name of the message queue
    """
    return resilient_service(
        service_name=f"message_queue_{queue_name}",
        circuit_breaker_config={
            'failure_threshold': 3,
            'recovery_timeout': 30,
            'expected_exception': Exception
        },
        retry_config={
            'max_attempts': 5,
            'base_delay': 0.5,
            'max_delay': 15.0,
            'exponential_base': 1.5,
            'jitter': True,
            'retryable_exceptions': (Exception,)
        }
    )

def resilient_payment_gateway(gateway_name: str):
    """
    Decorator for payment gateway operations with resilience patterns
    
    Args:
        gateway_name: Name of the payment gateway
    """
    return resilient_service(
        service_name=f"payment_gateway_{gateway_name}",
        circuit_breaker_config={
            'failure_threshold': 3,
            'recovery_timeout': 120,  # Longer recovery time for payment gateways
            'expected_exception': Exception
        },
        retry_config={
            'max_attempts': 2,  # Fewer retries for payment operations
            'base_delay': 2.0,
            'max_delay': 10.0,
            'exponential_base': 2.0,
            'jitter': True,
            'retryable_exceptions': (Exception,)
        }
    )

def timeout(seconds: float):
    """
    Decorator to add timeout to function calls
    
    Args:
        seconds: Timeout in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal
            import threading
            import time
            
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(seconds)
            
            if thread.is_alive():
                logger.warning(f"Function {func.__name__} timed out after {seconds} seconds")
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        
        return wrapper
    
    return decorator

def rate_limit(calls_per_second: float):
    """
    Decorator to rate limit function calls
    
    Args:
        calls_per_second: Maximum calls per second
    """
    def decorator(func: Callable) -> Callable:
        import time
        import threading
        
        last_called = [0.0]
        min_interval = 1.0 / calls_per_second
        lock = threading.Lock()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                now = time.time()
                time_since_last_call = now - last_called[0]
                
                if time_since_last_call < min_interval:
                    sleep_time = min_interval - time_since_last_call
                    logger.debug(f"Rate limiting: sleeping for {sleep_time:.3f} seconds")
                    time.sleep(sleep_time)
                
                last_called[0] = time.time()
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def bulkhead(max_concurrent: int):
    """
    Decorator to implement bulkhead pattern (limit concurrent executions)
    
    Args:
        max_concurrent: Maximum number of concurrent executions
    """
    def decorator(func: Callable) -> Callable:
        import threading
        import time
        
        semaphore = threading.Semaphore(max_concurrent)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not semaphore.acquire(blocking=False):
                logger.warning(f"Bulkhead limit reached for {func.__name__}, rejecting request")
                raise Exception(f"Bulkhead limit reached for {func.__name__}")
            
            try:
                return func(*args, **kwargs)
            finally:
                semaphore.release()
        
        return wrapper
    
    return decorator

def health_check(service_name: str):
    """
    Decorator to add health check functionality
    
    Args:
        service_name: Name of the service
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                # Update health status
                resilience_manager.get_circuit_breaker(service_name)._on_success()
                return result
            except Exception as e:
                # Update health status
                resilience_manager.get_circuit_breaker(service_name)._on_failure()
                raise e
        
        return wrapper
    
    return decorator

