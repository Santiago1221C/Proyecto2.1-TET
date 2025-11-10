package main.java.com.bookstore.user.config;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    @Bean
    public TopicExchange paymentExchange() {
        return new TopicExchange("payment_exchange", true, false);
    }

    @Bean
    public Queue userPaymentQueue() {
        return new Queue("user_payment_q", true);
    }

    @Bean
    public Binding bindingUserQueue(Queue userPaymentQueue, TopicExchange paymentExchange) {
        return BindingBuilder.bind(userPaymentQueue).to(paymentExchange).with("payment.*");
    }
}