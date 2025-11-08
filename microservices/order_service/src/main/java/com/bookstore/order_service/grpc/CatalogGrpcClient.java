package com.bookstore.order_service.grpc;

import com.bookstore.catalog.grpc.CatalogServiceGrpc;
import com.bookstore.catalog.grpc.DecreaseStockRequest;
import com.bookstore.catalog.grpc.StockUpdateResponse;
import net.devh.boot.grpc.client.inject.GrpcClient;
import org.springframework.stereotype.Service;

@Service
public class CatalogGrpcClient {

    @GrpcClient("catalog-service")
    private CatalogServiceGrpc.CatalogServiceBlockingStub blockingStub;

    public boolean decreaseStock(Long bookId, int quantity){
        System.out.println("Enviando solicitud gRPC al catálogo para decrementar stock del libro con ID: " + bookId);

        DecreaseStockRequest request = DecreaseStockRequest.newBuilder()
                .setBookId(bookId)
                .setQuantity(quantity)
                .build();

        StockUpdateResponse response = blockingStub.decreaseStock(request);

        return response.getSuccess();
    }   
}