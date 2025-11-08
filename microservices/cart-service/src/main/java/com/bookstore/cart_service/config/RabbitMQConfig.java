package com.bookstore.cart_service.config;

import org.springframework.amqp.core.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    public static final String CART_EXCHANGE = "cart.exchange";
    public static final String CART_ROUTING_KEY = "cart.updated";
    public static final String CART_QUEUE = "cart.events";

    @Bean
    public Queue cartQueue() {
        return QueueBuilder.durable(CART_QUEUE).build(); // 🔧 corregido: era ORDER_QUEUE
    }

    @Bean
    public TopicExchange cartExchange() {
        return new TopicExchange(CART_EXCHANGE);
    }

    @Bean
    public Binding binding(Queue cartQueue, TopicExchange cartExchange) {
        return BindingBuilder.bind(cartQueue).to(cartExchange).with(CART_ROUTING_KEY);
    }
}