package com.bookstore.user.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Generic Message Response DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class MessageResponse {

    private String message;
    private Boolean success;

    public MessageResponse(String message) {
        this.message = message;
        this.success = true;
    }
}


