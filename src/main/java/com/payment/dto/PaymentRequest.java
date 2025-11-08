package com.payment.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;

/**
 * Payment Request DTO
 * Data Transfer Object for payment creation requests
 */
public class PaymentRequest {
    
    @NotBlank(message = "Order ID is required")
    @Pattern(regexp = "^[A-Za-z0-9_-]+$", message = "Order ID must contain only alphanumeric characters, hyphens, and underscores")
    @JsonProperty("order_id")
    private String orderId;
    
    @NotBlank(message = "User ID is required")
    @Pattern(regexp = "^[A-Za-z0-9_-]+$", message = "User ID must contain only alphanumeric characters, hyphens, and underscores")
    @JsonProperty("user_id")
    private String userId;
    
    @NotNull(message = "Amount is required")
    @DecimalMin(value = "0.01", message = "Amount must be greater than 0")
    @DecimalMax(value = "1000000.00", message = "Amount exceeds maximum limit")
    private BigDecimal amount;
    
    @Pattern(regexp = "USD|EUR|GBP|CAD|AUD", message = "Invalid currency")
    private String currency = "USD";
    
    @Pattern(regexp = "credit_card|debit_card|paypal|bank_transfer", 
             message = "Invalid payment method")
    @JsonProperty("payment_method")
    private String paymentMethod = "credit_card";
    
    // Constructors
    public PaymentRequest() {}
    
    public PaymentRequest(String orderId, String userId, BigDecimal amount, 
                         String currency, String paymentMethod) {
        this.orderId = orderId;
        this.userId = userId;
        this.amount = amount;
        this.currency = currency;
        this.paymentMethod = paymentMethod;
    }
    
    // Getters and Setters
    public String getOrderId() {
        return orderId;
    }
    
    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }
    
    public String getUserId() {
        return userId;
    }
    
    public void setUserId(String userId) {
        this.userId = userId;
    }
    
    public BigDecimal getAmount() {
        return amount;
    }
    
    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }
    
    public String getCurrency() {
        return currency;
    }
    
    public void setCurrency(String currency) {
        this.currency = currency;
    }
    
    public String getPaymentMethod() {
        return paymentMethod;
    }
    
    public void setPaymentMethod(String paymentMethod) {
        this.paymentMethod = paymentMethod;
    }
    
    @Override
    public String toString() {
        return "PaymentRequest{" +
                "orderId='" + orderId + '\'' +
                ", userId='" + userId + '\'' +
                ", amount=" + amount +
                ", currency='" + currency + '\'' +
                ", paymentMethod='" + paymentMethod + '\'' +
                '}';
    }
}

