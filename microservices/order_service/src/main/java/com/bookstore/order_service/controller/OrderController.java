package com.bookstore.order_service.controller;

import com.bookstore.order_service.model.Order;
import com.bookstore.order_service.model.OrderStatus;
import com.bookstore.order_service.service.OrderService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService){
        this.orderService = orderService;
    }

    // Creación de una nueva orden desde el carrito del usuario
    @PostMapping("/{userId}")
    public ResponseEntity<Order> createOrderFromCart(@PathVariable Long userId){
        try {
            Order createdOrder = orderService.createOrderFromCart(userId);
            return ResponseEntity.ok(createdOrder);
        } catch (RuntimeException ex){
            return ResponseEntity.badRequest().body(null);
        }
    }

    // Obtener todas las órdenes
    @GetMapping
    public ResponseEntity<List<Order>> getAllOrders(){
        List<Order> orders = orderService.getAllOrders();
        return ResponseEntity.ok(orders);
    }

    // Obtener order por id
    @GetMapping("/{id}")
    public ResponseEntity<Order> getOrderById(@PathVariable Long id){
        return orderService.getOrderById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    // Obtener órdenes por usuario
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Order>> getOrdersByUser(@PathVariable Long userId){
        List<Order> orders = orderService.getOrdersByUser(userId);
        return ResponseEntity.ok(orders);
    }

    // Actualizar estado de una orden
    @PatchMapping("/{id}/status")
    public ResponseEntity<Order> updateOrderStatus(@PathVariable Long id, @RequestParam String status){
        try {
            OrderStatus newStatus = OrderStatus.valueOf(status.toUpperCase());
            Order updated = orderService.updateOrderStatus(id, newStatus);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException ex) {
            return ResponseEntity.badRequest().build(); // Status inválido
        } catch (RuntimeException ex) {
            return ResponseEntity.notFound().build();
        }
    }

    // Eliminar una orden
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteOrder(@PathVariable Long id){
        orderService.deleteOrder(id);
        return ResponseEntity.noContent().build();
    }
}