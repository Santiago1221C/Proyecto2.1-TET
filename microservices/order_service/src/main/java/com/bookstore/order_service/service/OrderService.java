package com.bookstore.order_service.service;

import com.bookstore.order_service.grpc.CatalogGrpcClient;
import com.bookstore.order_service.grpc.CartGrpcClient;
import com.bookstore.order_service.messaging.OrderEventPublisher;
import com.bookstore.order_service.model.Order;
import com.bookstore.order_service.model.OrderItem;
import com.bookstore.order_service.model.OrderStatus;
import com.bookstore.order_service.repository.OrderRepository;
import com.bookstore.order_service.config.RabbitMQConfig;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final CatalogGrpcClient catalogGrpcClient;
    private final CartGrpcClient cartGrpcClient;
    private final OrderEventPublisher orderEventPublisher;

    

    public OrderService(OrderRepository orderRepository, CatalogGrpcClient catalogGrpcClient, CartGrpcClient cartGrpcClient, OrderEventPublisher orderEventPublisher){
        this.orderRepository = orderRepository;
        this.catalogGrpcClient = catalogGrpcClient;
        this.cartGrpcClient = cartGrpcClient;
        this.orderEventPublisher = orderEventPublisher;
    }

    // Crear una nueva orden para un usuario

    @Transactional
    public Order createOrderFromCart(Long userId){
        System.out.println("Obteniendo carrito para el usuario con ID: " + userId);

        var cartResponse = cartGrpcClient.getCartByUserId(userId);

        if (cartResponse == null || cartResponse.getItemsList().isEmpty()){
            throw new RuntimeException("El carrito está vacío o no existe para el usuario: " + userId);
        }

        System.out.println("Carrito encontrado con " + cartResponse.getItemsList().size() + " items.");

        // Convertimos los items del carrito en items de orden

        List<OrderItem> orderItems = cartResponse.getItemsList().stream().map(i -> new OrderItem(i.getBookId(), i.getTitle(), i.getAuthor(), i.getPrice(), i.getQuantity())).collect(Collectors.toList());

        // Creación de la nueva orden

        Order order = new Order();
        order.setUserId(userId);
        order.setItems(orderItems);
        order.setStatus(OrderStatus.CREATED);
        order.setCreatedAt(LocalDateTime.now());
        order.setUpdatedAt(LocalDateTime.now());
        // Calcular el total del pedido
        order.recalculateTotal();

        // Relacion bidireccional
        for (OrderItem item : orderItems){
            item.setOrder(order);
        }

        // Guardar la orden en la base de datos
        Order savedOrder = orderRepository.save(order);
        System.out.println("Orden creada con ID: " + savedOrder.getId());

        System.out.println("Creando orden para el usuario: " + userId + " con total de: " + order.getTotalPrice());

        // Llamada al servicio de catálogo para disminuir el stock
        for (OrderItem item : savedOrder.getItems()) {
            boolean success = catalogGrpcClient.decreaseStock(item.getBookId(), item.getQuantity());

            if (!success){
                System.err.println("No se pudo actualizar el stock para el libro con ID: " + item.getBookId());
            } else {
                System.out.println("Stock actualizado correctamente para el libro con ID: " +  item.getBookId());
            }
        }

        // Publicar evento en RabbitMQ
        for (OrderItem item : savedOrder.getItems()) {
            orderEventPublisher.publishOrderCreated(item.getBookId(), item.getQuantity());
        }

        // Limpiar carrito después de crear la orden
        boolean cleared = cartGrpcClient.clearCart(userId);
        if (!cleared) {
            System.err.println("No se pudo limpiar el carrito del usuario " + userId);
        } else {
            System.out.println("Carrito limpiado correctamente para el usuario " + userId);
        }

        return savedOrder;
    }

    @Transactional(readOnly = true)
    public List<Order> getAllOrders() {
        return orderRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Optional<Order> getOrderById(Long id){
        return orderRepository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Order> getOrdersByUser(Long userId){
        return orderRepository.findByUserId(userId);
    }

    // Actualiza el estado de una orden
    @Transactional
    public Order updateOrderStatus(Long orderId, OrderStatus newStatus){
        Order order = orderRepository.findById(orderId).orElseThrow(() -> new RuntimeException("Orden no encontrada con ID: " + orderId));
        order.setStatus(newStatus);
        order.setUpdatedAt(LocalDateTime.now());

        return orderRepository.save(order);
    }

    @Transactional
    public void deleteOrder(Long orderId){
        System.out.println("Eliminando orden con ID: " + orderId);
        orderRepository.deleteById(orderId);
    }
}