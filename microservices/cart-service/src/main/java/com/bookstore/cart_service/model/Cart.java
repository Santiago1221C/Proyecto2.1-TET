package com.bookstore.cart_service.model;

import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;
import com.fasterxml.jackson.annotation.JsonManagedReference;

@Entity
@Table(name = "carts")
public class Cart {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private Long userId;

    @Column(nullable = false)
    private Double totalPrice = 0.0;

    @OneToMany(mappedBy = "cart", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    @JsonManagedReference
    private List<CartItem> items = new ArrayList<>();

    public Cart(){

    }

    public Cart(Long userId){
        this.userId = userId;
        this.totalPrice = 0.0;
    }

    // Métodos auxiliares
    public void addItem(CartItem item){
        item.setCart(this);
        this.items.add(item);
        recalculateTotal();
    }

    public void removeItem(CartItem item){
        this.items.remove(item);
        item.setCart(null);
        recalculateTotal();
    }

    public void recalculateTotal(){
        this.totalPrice = this.items.stream().mapToDouble(i -> i.getPrice() * i.getQuantity()).sum();
    }

    public double calculateTotalPrice(){
        return items.stream().mapToDouble(i -> i.getPrice() * i.getQuantity()).sum();
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

    public List<CartItem> getItems() {
        return items;
    }

    public void setItems(List<CartItem> items) {
        this.items = items;
    }

    public Double getTotalPrice() {
        return totalPrice;
    }

    public void setTotalPrice(Double totalPrice) {
        this.totalPrice = totalPrice;
    }
}