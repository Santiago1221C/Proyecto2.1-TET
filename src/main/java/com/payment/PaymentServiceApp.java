package com.payment;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Payment Service Application
 * Microservice for handling payment processing with RabbitMQ integration
 * 
 * Features:
 * - REST API for payment operations
 * - RabbitMQ message publishing and consuming
 * - Payment validation and processing
 * - Integration with other microservices
 * 
 * @author Bookstore Microservices Architecture
 * @version 1.0.0
 */
@SpringBootApplication
@EnableEurekaClient
@EnableAsync
public class PaymentServiceApp {
    
    public static void main(String[] args) {
        SpringApplication.run(PaymentServiceApp.class, args);
    }
}
