package com.bookstore.order_service.model;

public enum OrderStatus {
    CREATED,    // Pedido recién creado
    PAID,       // Pagado
    SHIPPED,    // Enviado
    DELIVERED,  // Entregado
    CANCELLED   // Cancelado
}