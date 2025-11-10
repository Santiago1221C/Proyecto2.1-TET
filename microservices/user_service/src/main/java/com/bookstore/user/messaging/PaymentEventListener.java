package main.java.com.bookstore.user.messaging;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class PaymentEventListener {

    @RabbitListener(queues = "user_payment_q")
    public void handlePaymentEvents(String message) {
        System.out.println("[user_service] Received payment event: " + message);
    }
}