package com.bookstore.cart_service.grpc;

import com.bookstore.catalog.grpc.CatalogServiceGrpc;
import com.bookstore.catalog.grpc.CheckStockRequest;
import com.bookstore.catalog.grpc.CheckStockResponse;
import com.bookstore.catalog.grpc.GetBookRequest;
import com.bookstore.catalog.grpc.BookResponse;
import net.devh.boot.grpc.client.inject.GrpcClient;
import org.springframework.stereotype.Service;

@Service
public class CatalogGrpcClient {

    @GrpcClient("catalog-service")
    private CatalogServiceGrpc.CatalogServiceBlockingStub blockingStub;

    // Obtener información de un libro por ID
    public BookResponse getBookById(long bookId){
        GetBookRequest request = GetBookRequest.newBuilder()
                .setBookId(bookId)
                .build();
        
        return blockingStub.getBookById(request);
    }

    // Verificar disponibilidad del stock antes de agregar al carrito
    public boolean checkStock(long bookId, int quantity){
        CheckStockRequest request = CheckStockRequest.newBuilder()
                .setBookId(bookId)
                .setRequestedQuantity(quantity)
                .build();
        
        CheckStockResponse response = blockingStub.checkStock(request);
        return response.getAvailable();
    }
}