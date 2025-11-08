package com.bookstore.order_service.dto;

import java.util.List;

public class OrderRequest {

    private Long userId;
    private List<OrderItemRequest> items;

    public static class OrderItemRequest {
        private Long bookId;
        private String title;
        private String author;
        private Double price;
        private int quantity;

        // Getters y Setters
        public Long getBookId() {
            return bookId;
        }
        public void setBookId(Long bookId) {
            this.bookId = bookId;
        }
        public String getTitle() {
            return title;
        }
        public void setTitle(String title) {
            this.title = title;
        }
        public String getAuthor(){
            return author;
        }
        public void setAuthor(String author){
            this.author = author;
        }
        public Double getPrice() {
            return price;
        }
        public void setPrice(Double price) {
            this.price = price;
        }
        public int getQuantity() {
            return quantity;
        }
        public void setQuantity(int quantity) {
            this.quantity = quantity;
        }
    }

    // Getters y Setters
    public Long getUserId(){
        return userId;
    }

    public void setUserId(Long userId){
        this.userId = userId;
    }

    public List<OrderItemRequest> getItems(){
        return items;
    }

    public void setItems(List<OrderItemRequest> items){
        this.items = items;
    }   
}