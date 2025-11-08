package com.bookstore.catalog.messaging;

import com.bookstore.catalog.config.RabbitMQConfig;
import com.bookstore.catalog.repository.BookRepository;
import com.bookstore.catalog.model.Book;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Optional;

@Service
public class OrderEventListener {

    private static final Logger logger = LoggerFactory.getLogger(OrderEventListener.class);
    private final BookRepository bookRepository;

    public OrderEventListener(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    @RabbitListener(queues = RabbitMQConfig.ORDER_QUEUE)
    public void handleOrderCreated(String message) {
        logger.info("[CatalogService] Mensaje recibido desde RabbitMQ: {}", message);

        // Esperamos formato: "bookId:quantity"
        try {
            String[] parts = message.split(":");
            Long bookId = Long.parseLong(parts[0]);
            int quantity = Integer.parseInt(parts[1]);

            Optional<Book> optionalBook = bookRepository.findById(bookId);
            if (optionalBook.isPresent()) {
                Book book = optionalBook.get();
                if (book.getStock() >= quantity) {
                    book.setStock(book.getStock() - quantity);
                    bookRepository.save(book);
                    logger.info("Stock actualizado para '{}': nuevo stock = {}", book.getTitle(), book.getStock());
                } else {
                    logger.warn("Stock insuficiente para '{}'. Disponible: {}, solicitado: {}", book.getTitle(), book.getStock(), quantity);
                }
            } else {
                logger.error("Libro no encontrado con ID {}", bookId);
            }
        } catch (Exception e) {
            logger.error("Error procesando mensaje: {}", message, e);
        }
    }
}