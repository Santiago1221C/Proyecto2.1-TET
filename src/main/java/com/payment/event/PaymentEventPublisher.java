package com.payment.event;

import com.payment.model.Payment;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Payment Event Publisher
 * Publishes payment events to RabbitMQ
 */
@Component
public class PaymentEventPublisher {
    
    private static final Logger logger = LoggerFactory.getLogger(PaymentEventPublisher.class);
    
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    @Value("${rabbitmq.exchange.payment}")
    private String paymentExchange;
    
    @Value("${rabbitmq.routing-key.payment.completed}")
    private String paymentCompletedRoutingKey;
    
    @Value("${rabbitmq.routing-key.payment.failed}")
    private String paymentFailedRoutingKey;
    
    @Value("${rabbitmq.routing-key.payment.refunded}")
    private String paymentRefundedRoutingKey;
    
    /**
     * Publish payment completed event
     * 
     * @param payment Payment entity
     */
    public void publishPaymentCompletedEvent(Payment payment) {
        try {
            PaymentEvent event = new PaymentEvent(
                "payment.completed",
                "payment-service",
                payment.getPaymentId(),
                payment.getOrderId(),
                payment.getUserId(),
                payment.getAmount(),
                payment.getCurrency(),
                payment.getStatus().getValue(),
                payment.getTransactionId(),
                payment.getMessage()
            );
            
            rabbitTemplate.convertAndSend(paymentExchange, paymentCompletedRoutingKey, event);
            logger.info("Published payment completed event for payment: {}", payment.getPaymentId());
            
        } catch (Exception e) {
            logger.error("Failed to publish payment completed event: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to publish payment completed event", e);
        }
    }
    
    /**
     * Publish payment failed event
     * 
     * @param payment Payment entity
     */
    public void publishPaymentFailedEvent(Payment payment) {
        try {
            PaymentEvent event = new PaymentEvent(
                "payment.failed",
                "payment-service",
                payment.getPaymentId(),
                payment.getOrderId(),
                payment.getUserId(),
                payment.getAmount(),
                payment.getCurrency(),
                payment.getStatus().getValue(),
                payment.getTransactionId(),
                payment.getMessage()
            );
            
            rabbitTemplate.convertAndSend(paymentExchange, paymentFailedRoutingKey, event);
            logger.info("Published payment failed event for payment: {}", payment.getPaymentId());
            
        } catch (Exception e) {
            logger.error("Failed to publish payment failed event: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to publish payment failed event", e);
        }
    }
    
    /**
     * Publish payment refunded event
     * 
     * @param payment Payment entity
     */
    public void publishPaymentRefundedEvent(Payment payment) {
        try {
            PaymentEvent event = new PaymentEvent(
                "payment.refunded",
                "payment-service",
                payment.getPaymentId(),
                payment.getOrderId(),
                payment.getUserId(),
                payment.getAmount(),
                payment.getCurrency(),
                payment.getStatus().getValue(),
                payment.getTransactionId(),
                payment.getMessage()
            );
            
            rabbitTemplate.convertAndSend(paymentExchange, paymentRefundedRoutingKey, event);
            logger.info("Published payment refunded event for payment: {}", payment.getPaymentId());
            
        } catch (Exception e) {
            logger.error("Failed to publish payment refunded event: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to publish payment refunded event", e);
        }
    }
    
    /**
     * Payment Event DTO
     */
    public static class PaymentEvent {
        private String eventType;
        private String service;
        private String paymentId;
        private String orderId;
        private String userId;
        private java.math.BigDecimal amount;
        private String currency;
        private String status;
        private String transactionId;
        private String message;
        private java.time.LocalDateTime timestamp;
        
        public PaymentEvent() {
            this.timestamp = java.time.LocalDateTime.now();
        }
        
        public PaymentEvent(String eventType, String service, String paymentId, 
                           String orderId, String userId, java.math.BigDecimal amount, 
                           String currency, String status, String transactionId, String message) {
            this();
            this.eventType = eventType;
            this.service = service;
            this.paymentId = paymentId;
            this.orderId = orderId;
            this.userId = userId;
            this.amount = amount;
            this.currency = currency;
            this.status = status;
            this.transactionId = transactionId;
            this.message = message;
        }
        
        // Getters and Setters
        public String getEventType() { return eventType; }
        public void setEventType(String eventType) { this.eventType = eventType; }
        
        public String getService() { return service; }
        public void setService(String service) { this.service = service; }
        
        public String getPaymentId() { return paymentId; }
        public void setPaymentId(String paymentId) { this.paymentId = paymentId; }
        
        public String getOrderId() { return orderId; }
        public void setOrderId(String orderId) { this.orderId = orderId; }
        
        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }
        
        public java.math.BigDecimal getAmount() { return amount; }
        public void setAmount(java.math.BigDecimal amount) { this.amount = amount; }
        
        public String getCurrency() { return currency; }
        public void setCurrency(String currency) { this.currency = currency; }
        
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        
        public String getTransactionId() { return transactionId; }
        public void setTransactionId(String transactionId) { this.transactionId = transactionId; }
        
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        
        public java.time.LocalDateTime getTimestamp() { return timestamp; }
        public void setTimestamp(java.time.LocalDateTime timestamp) { this.timestamp = timestamp; }
    }
}

