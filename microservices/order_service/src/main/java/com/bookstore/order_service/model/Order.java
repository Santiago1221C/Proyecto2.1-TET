package com.bookstore.order_service.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false)
    private Double totalPrice = 0.0;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private OrderStatus status = OrderStatus.CREATED;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(nullable = false)
    private LocalDateTime updatedAt = LocalDateTime.now();

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();
    

    public Order(){

    }

    public Order(Long userId, Double totalPrice, List<OrderItem> items){
        this.userId = userId;
        this.totalPrice = totalPrice;
        this.status = OrderStatus.CREATED;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
        this.items = items != null ? items : new ArrayList<>();
    }

    // Métodos de negocio

    // Agregar item correctamente
    public void addItem(OrderItem item){
        item.setOrder(this);
        this.items.add(item);
        recalculateTotal();
    }

    // Actualizar estado de la orden
    public void updateStatus(OrderStatus newStatus){
        this.status = newStatus;
        this.updatedAt = LocalDateTime.now();
    }

    // Recalcular total (si se eliminan o agregan items)
    public void recalculateTotal(){
        this.totalPrice = this.items.stream().mapToDouble(i -> i.getPrice() * i.getQuantity()).sum();
    }

    // Getters y Setters
    public Long getId() {
        return id;
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

    public OrderStatus getStatus() {
        return status;
    }

    public void setStatus(OrderStatus status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setItems(List<OrderItem> items) {
        this.items.clear();
        if (items != null){
            items.forEach(this::addItem);
        }
    }    
}