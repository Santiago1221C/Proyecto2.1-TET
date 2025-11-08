package com.payment.model;

/**
 * Payment Status Enumeration
 * Defines the possible states of a payment transaction
 */
public enum PaymentStatus {
    
    /**
     * Payment is pending processing
     */
    PENDING("pending"),
    
    /**
     * Payment has been completed successfully
     */
    COMPLETED("completed"),
    
    /**
     * Payment has failed
     */
    FAILED("failed"),
    
    /**
     * Payment has been refunded
     */
    REFUNDED("refunded"),
    
    /**
     * Payment has been cancelled
     */
    CANCELLED("cancelled");
    
    private final String value;
    
    PaymentStatus(String value) {
        this.value = value;
    }
    
    public String getValue() {
        return value;
    }
    
    @Override
    public String toString() {
        return value;
    }
    
    /**
     * Get PaymentStatus from string value
     * 
     * @param value String value
     * @return PaymentStatus enum or null if not found
     */
    public static PaymentStatus fromValue(String value) {
        for (PaymentStatus status : PaymentStatus.values()) {
            if (status.value.equalsIgnoreCase(value)) {
                return status;
            }
        }
        return null;
    }
}

