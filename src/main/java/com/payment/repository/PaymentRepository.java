package com.payment.repository;

import com.payment.model.Payment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Payment Repository
 * Data access layer for Payment entities
 */
@Repository
public interface PaymentRepository extends JpaRepository<Payment, Long> {
    
    /**
     * Find payment by payment ID
     * 
     * @param paymentId Payment ID
     * @return Payment entity or null if not found
     */
    Payment findByPaymentId(String paymentId);
    
    /**
     * Find payments by user ID
     * 
     * @param userId User ID
     * @return List of payments for the user
     */
    List<Payment> findByUserId(String userId);
    
    /**
     * Find payments by order ID
     * 
     * @param orderId Order ID
     * @return List of payments for the order
     */
    List<Payment> findByOrderId(String orderId);
    
    /**
     * Find payments by status
     * 
     * @param status Payment status
     * @return List of payments with the specified status
     */
    List<Payment> findByStatus(String status);
    
    /**
     * Find payments by user ID and status
     * 
     * @param userId User ID
     * @param status Payment status
     * @return List of payments for the user with the specified status
     */
    List<Payment> findByUserIdAndStatus(String userId, String status);
    
    /**
     * Count payments by user ID
     * 
     * @param userId User ID
     * @return Number of payments for the user
     */
    long countByUserId(String userId);
    
    /**
     * Find payments by user ID ordered by creation date descending
     * 
     * @param userId User ID
     * @return List of payments ordered by creation date descending
     */
    @Query("SELECT p FROM Payment p WHERE p.userId = :userId ORDER BY p.createdAt DESC")
    List<Payment> findByUserIdOrderByCreatedAtDesc(@Param("userId") String userId);
    
    /**
     * Find payments by date range
     * 
     * @param startDate Start date
     * @param endDate End date
     * @return List of payments within the date range
     */
    @Query("SELECT p FROM Payment p WHERE p.createdAt BETWEEN :startDate AND :endDate ORDER BY p.createdAt DESC")
    List<Payment> findByDateRange(@Param("startDate") java.time.LocalDateTime startDate, 
                                 @Param("endDate") java.time.LocalDateTime endDate);
    
    /**
     * Find payments by amount range
     * 
     * @param minAmount Minimum amount
     * @param maxAmount Maximum amount
     * @return List of payments within the amount range
     */
    @Query("SELECT p FROM Payment p WHERE p.amount BETWEEN :minAmount AND :maxAmount ORDER BY p.createdAt DESC")
    List<Payment> findByAmountRange(@Param("minAmount") java.math.BigDecimal minAmount, 
                                   @Param("maxAmount") java.math.BigDecimal maxAmount);
}

