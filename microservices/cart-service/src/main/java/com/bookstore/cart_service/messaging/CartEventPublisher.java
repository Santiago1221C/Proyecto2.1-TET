package com.bookstore.cart_service.event;

import com.bookstore.cart_service.config.RabbitMQConfig;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;

@Component
public class CartEventPublisher {

    private final RabbitTemplate rabbitTemplate;

    public CartEventPublisher(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void publishCartUpdated(Long userId, String action) {
        String message = String.format("El carrito del usuario %d ha sido %s.", userId, action);
        rabbitTemplate.convertAndSend(RabbitMQConfig.CART_EXCHANGE, RabbitMQConfig.CART_ROUTING_KEY, message);
        System.out.println("[RabbitMQ] Evento enviado: " + message);
    }
}