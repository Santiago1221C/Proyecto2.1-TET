package com.payment.service;

import com.payment.dto.PaymentRequest;
import com.payment.dto.PaymentResponse;
import com.payment.model.Payment;
import com.payment.model.PaymentStatus;
import com.payment.repository.PaymentRepository;
import com.payment.event.PaymentEventPublisher;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Payment Service
 * Business logic for payment processing
 */
@Service
@Transactional
public class PaymentService {
    
    private static final Logger logger = LoggerFactory.getLogger(PaymentService.class);
    
    @Autowired
    private PaymentRepository paymentRepository;
    
    @Autowired
    private PaymentEventPublisher eventPublisher;
    
    // Payment processing configuration
    private static final double PAYMENT_SUCCESS_RATE = 0.85; // 85% success rate
    private static final int PAYMENT_PROCESSING_TIME_MS = 2000; // 2 seconds
    
    /**
     * Process a payment request
     * 
     * @param paymentRequest Payment request data
     * @return Payment response
     */
    public PaymentResponse processPayment(PaymentRequest paymentRequest) {
        logger.info("Processing payment for order: {}", paymentRequest.getOrderId());
        
        try {
            // Create payment entity
            Payment payment = new Payment(
                paymentRequest.getOrderId(),
                paymentRequest.getUserId(),
                paymentRequest.getAmount(),
                paymentRequest.getCurrency(),
                paymentRequest.getPaymentMethod()
            );
            
            // Simulate payment processing time
            Thread.sleep(PAYMENT_PROCESSING_TIME_MS);
            
            // Simulate payment gateway response
            boolean success = Math.random() < PAYMENT_SUCCESS_RATE;
            
            if (success) {
                payment.setStatus(PaymentStatus.COMPLETED);
                payment.setTransactionId("TXN-" + UUID.randomUUID().toString().substring(0, 12).toUpperCase());
                payment.setMessage("Payment processed successfully");
            } else {
                payment.setStatus(PaymentStatus.FAILED);
                payment.setMessage("Payment declined by gateway");
            }
            
            // Save payment
            payment = paymentRepository.save(payment);
            
            // Publish payment event
            try {
                if (payment.getStatus() == PaymentStatus.COMPLETED) {
                    eventPublisher.publishPaymentCompletedEvent(payment);
                } else if (payment.getStatus() == PaymentStatus.FAILED) {
                    eventPublisher.publishPaymentFailedEvent(payment);
                }
            } catch (Exception e) {
                logger.warn("Failed to publish payment event: {}", e.getMessage());
                // Don't fail the payment if event publishing fails
            }
            
            logger.info("Payment {} processed with status: {}", 
                payment.getPaymentId(), payment.getStatus());
            
            return convertToResponse(payment);
            
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            logger.error("Payment processing interrupted: {}", e.getMessage());
            throw new RuntimeException("Payment processing interrupted", e);
        } catch (Exception e) {
            logger.error("Error processing payment: {}", e.getMessage(), e);
            throw new RuntimeException("Payment processing failed", e);
        }
    }
    
    /**
     * Get payment by ID
     * 
     * @param paymentId Payment ID
     * @return Payment response or null if not found
     */
    @Transactional(readOnly = true)
    public PaymentResponse getPaymentById(String paymentId) {
        logger.info("Retrieving payment: {}", paymentId);
        
        try {
            Payment payment = paymentRepository.findByPaymentId(paymentId);
            
            if (payment != null) {
                return convertToResponse(payment);
            }
            
            return null;
            
        } catch (Exception e) {
            logger.error("Error retrieving payment: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to retrieve payment", e);
        }
    }
    
    /**
     * Get payments by user ID
     * 
     * @param userId User ID
     * @return List of payment responses
     */
    @Transactional(readOnly = true)
    public List<PaymentResponse> getPaymentsByUserId(String userId) {
        logger.info("Retrieving payments for user: {}", userId);
        
        try {
            List<Payment> payments = paymentRepository.findByUserId(userId);
            
            return payments.stream()
                .map(this::convertToResponse)
                .collect(Collectors.toList());
                
        } catch (Exception e) {
            logger.error("Error retrieving user payments: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to retrieve user payments", e);
        }
    }
    
    /**
     * Refund a payment
     * 
     * @param paymentId Payment ID to refund
     * @return Payment response
     */
    public PaymentResponse refundPayment(String paymentId) {
        logger.info("Refunding payment: {}", paymentId);
        
        try {
            Payment payment = paymentRepository.findByPaymentId(paymentId);
            
            if (payment == null) {
                throw new RuntimeException("Payment not found");
            }
            
            if (payment.getStatus() != PaymentStatus.COMPLETED) {
                throw new RuntimeException("Only completed payments can be refunded");
            }
            
            // Update payment status
            payment.setStatus(PaymentStatus.REFUNDED);
            payment.setMessage("Payment refunded successfully");
            payment = paymentRepository.save(payment);
            
            // Publish refund event
            try {
                eventPublisher.publishPaymentRefundedEvent(payment);
            } catch (Exception e) {
                logger.warn("Failed to publish refund event: {}", e.getMessage());
                // Don't fail the refund if event publishing fails
            }
            
            logger.info("Payment {} refunded successfully", paymentId);
            
            return convertToResponse(payment);
            
        } catch (Exception e) {
            logger.error("Error refunding payment: {}", e.getMessage(), e);
            throw new RuntimeException("Payment refund failed", e);
        }
    }
    
    /**
     * Convert Payment entity to PaymentResponse DTO
     * 
     * @param payment Payment entity
     * @return PaymentResponse DTO
     */
    private PaymentResponse convertToResponse(Payment payment) {
        return new PaymentResponse(
            payment.getPaymentId(),
            payment.getOrderId(),
            payment.getUserId(),
            payment.getAmount(),
            payment.getCurrency(),
            payment.getPaymentMethod(),
            payment.getStatus(),
            payment.getTransactionId(),
            payment.getMessage()
        );
    }
}

