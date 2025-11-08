package com.bookstore.order_service.grpc;

import com.bookstore.cart.grpc.CartServiceGrpc;
import com.bookstore.cart.grpc.ClearCartRequest;
import com.bookstore.cart.grpc.GetCartRequest;
import com.bookstore.cart.grpc.CartResponse;
import net.devh.boot.grpc.client.inject.GrpcClient;
import org.springframework.stereotype.Service;

@Service
public class CartGrpcClient {

    @GrpcClient("cart-service")
    private CartServiceGrpc.CartServiceBlockingStub cartStub;

    public CartResponse getCartByUserId(Long userId){
        GetCartRequest request = GetCartRequest.newBuilder()
                .setUserId(userId)
                .build();

        return cartStub.getCartByUser(request);
    }
    
    public boolean clearCart(Long userId){
        System.out.println("Enviando solicitud gRPC al carrito para limpiar items del usuario: " + userId);

        ClearCartRequest request = ClearCartRequest.newBuilder()
                .setUserId(userId)
                .build();

        CartResponse response = cartStub.clearCart(request);

        return response.getItemsCount() == 0; // true si quedó vacío
    }
}