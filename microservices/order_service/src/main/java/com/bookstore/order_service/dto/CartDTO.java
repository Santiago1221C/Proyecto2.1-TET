package com.bookstore.order_service.dto;

import java.util.List;

public class CartDTO {
    private Long id;
    private Long userId;
    private Double totalPrice;
    private List<CartItemDTO> items;

    // Getters y Setters

    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    public Long getUserId() {
        return userId;
    }
    public void setUserId(Long userId) {
        this.userId = userId;
    }
    public Double getTotalPrice() {
        return totalPrice;
    }
    public void setTotalPrice(Double totalPrice) {
        this.totalPrice = totalPrice;
    }
    public List<CartItemDTO> getItems() {
        return items;
    }
    public void setItems(List<CartItemDTO> items) {
        this.items = items;
    }
}