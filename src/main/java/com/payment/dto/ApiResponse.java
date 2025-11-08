package com.payment.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Generic API Response DTO
 * Standardized response format for all API endpoints
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {
    
    private String status;
    private String message;
    private T data;
    private List<String> errors;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
    private LocalDateTime timestamp;
    
    // Constructors
    public ApiResponse() {
        this.timestamp = LocalDateTime.now();
    }
    
    public ApiResponse(String status, String message) {
        this();
        this.status = status;
        this.message = message;
    }
    
    public ApiResponse(String status, String message, T data) {
        this(status, message);
        this.data = data;
    }
    
    public ApiResponse(String status, String message, T data, List<String> errors) {
        this(status, message, data);
        this.errors = errors;
    }
    
    // Static factory methods
    public static <T> ApiResponse<T> success(String message) {
        return new ApiResponse<>("success", message);
    }
    
    public static <T> ApiResponse<T> success(String message, T data) {
        return new ApiResponse<>("success", message, data);
    }
    
    public static <T> ApiResponse<T> error(String message) {
        return new ApiResponse<>("error", message);
    }
    
    public static <T> ApiResponse<T> error(String message, List<String> errors) {
        return new ApiResponse<>("error", message, null, errors);
    }
    
    public static <T> ApiResponse<T> validationError(String message, List<String> errors) {
        return new ApiResponse<>("validation_error", message, null, errors);
    }
    
    public static <T> ApiResponse<T> notFound(String message) {
        return new ApiResponse<>("not_found", message);
    }
    
    // Getters and Setters
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public T getData() {
        return data;
    }
    
    public void setData(T data) {
        this.data = data;
    }
    
    public List<String> getErrors() {
        return errors;
    }
    
    public void setErrors(List<String> errors) {
        this.errors = errors;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
    @Override
    public String toString() {
        return "ApiResponse{" +
                "status='" + status + '\'' +
                ", message='" + message + '\'' +
                ", data=" + data +
                ", errors=" + errors +
                ", timestamp=" + timestamp +
                '}';
    }
}

