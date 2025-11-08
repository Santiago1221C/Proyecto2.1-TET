package com.bookstore.catalog.grpc;

import com.bookstore.catalog.model.Book;
import com.bookstore.catalog.repository.BookRepository;
import net.devh.boot.grpc.server.service.GrpcService;

import io.grpc.stub.StreamObserver;
import org.springframework.beans.factory.annotation.Autowired;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Optional;

@GrpcService
public class CatalogGrpcService extends CatalogServiceGrpc.CatalogServiceImplBase {

    private static final Logger logger = LoggerFactory.getLogger(CatalogGrpcService.class);

    @Autowired
    private BookRepository bookRepository;

    @Override
    public void decreaseStock(DecreaseStockRequest request, StreamObserver<StockUpdateResponse> responseObserver){
        Long bookId = request.getBookId();
        int quantity = request.getQuantity();

        logger.info("Solicitud recibida por gRPC para disminuir el stock del libro con ID: {} en {} unidades", bookId, quantity);
        Optional<Book> optionalBook = bookRepository.findById(bookId);
        StockUpdateResponse.Builder response = StockUpdateResponse.newBuilder();

        if (optionalBook.isPresent()) {
            Book book = optionalBook.get();

            if (book.getStock() >= quantity) {
                book.setStock(book.getStock() - quantity);
                bookRepository.save(book);

                logger.info("Stock actualizado correctamente. Nuevo stock del libro '{}': {}", book.getTitle(), book.getStock());

                response.setSuccess(true)
                        .setMessage("Stock actualizado correctamente");
            } else {
                logger.warn("No hay suficiente stock para el libro '{}'. Stock actual: {}, solicitado: {}", book.getTitle(), book.getStock(), quantity);
                response.setSuccess(false)
                        .setMessage("No hay suficiente stock para el libro");
            }
        } else {
            logger.error("Libro no encontrado con ID: {}", bookId);
            response.setSuccess(false)
                    .setMessage("Libro no encontrado");
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }

    @Override
    public void checkStock(CheckStockRequest request, StreamObserver<CheckStockResponse> responseObserver){
        Long bookId = request.getBookId();
        int requestedQuantity = request.getRequestedQuantity();
        
        Optional<Book> optionalBook = bookRepository.findById(bookId);

        if (optionalBook.isEmpty()) {
            // Si no se encuentra el libro
            CheckStockResponse response = CheckStockResponse.newBuilder()
                    .setAvailable(false)
                    .setStock(0)
                    .setMessage("El libro con ID " + bookId + " no existe.")
                    .build();
            
            responseObserver.onNext(response);
            responseObserver.onCompleted();
            return;
        }

        Book book = optionalBook.get();
        int currentStock = book.getStock();

        boolean available = currentStock >= requestedQuantity;

        CheckStockResponse response = CheckStockResponse.newBuilder()
                .setAvailable(available)
                .setStock(currentStock)
                .setMessage(available
                        ? "Stock suficiente disponible (" + currentStock + " unidades)."
                        : "Stock insuficiente. Solo quedan " + currentStock + " unidades disponibles.")
                .build();
        
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    @Override
    public void getBookById(GetBookRequest request, StreamObserver<BookResponse> responseObserver){
        Long bookId = request.getBookId();
        logger.info("Solicitud recibida para obtener la información del libro con ID: {}", bookId);

        Optional<Book> optionalBook = bookRepository.findById(bookId);
        BookResponse.Builder response = BookResponse.newBuilder();

        if (optionalBook.isPresent()){
            Book book = optionalBook.get();
            response.setId(book.getId())
                    .setTitle(book.getTitle())
                    .setAuthor(book.getAuthor())
                    .setDescription(book.getDescription())
                    .setStock(book.getStock())
                    .setPrice(book.getPrice());
            logger.info("Libro encontrado: {}", book.getTitle());
        } else {
            logger.warn("No se encontró el libro con ID: {}", bookId);
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }
}