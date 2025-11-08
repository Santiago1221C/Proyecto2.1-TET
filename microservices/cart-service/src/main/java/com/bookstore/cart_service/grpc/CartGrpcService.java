package com.bookstore.cart_service.grpc;

import com.bookstore.cart.grpc.CartServiceGrpc;
import com.bookstore.cart.grpc.GetCartRequest;
import com.bookstore.cart.grpc.AddItemRequest;
import com.bookstore.cart.grpc.ClearCartRequest;
import com.bookstore.cart.grpc.CartResponse;
import com.bookstore.cart_service.model.Cart;
import com.bookstore.cart_service.model.CartItem;
import com.bookstore.cart_service.service.CartService;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;
import org.springframework.transaction.annotation.Transactional;

import java.util.stream.Collectors;

@GrpcService
public class CartGrpcService extends CartServiceGrpc.CartServiceImplBase {

    private final CartService cartService;

    public CartGrpcService(CartService cartService){
        this.cartService = cartService;
    }

    @Override
    @Transactional
    public void getCartByUser(GetCartRequest request, StreamObserver<CartResponse> responseObserver){
        Cart cart = cartService.getCartByUserId(request.getUserId());

        CartResponse response = CartResponse.newBuilder()
                .setUserId(cart.getUserId())
                .addAllItems(cart.getItems().stream().map(this::mapToProtoItem).collect(Collectors.toList()))
                .setTotalPrice(cart.calculateTotalPrice())
                .build();
        
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    @Override
    @Transactional
    public void addItemToCart(AddItemRequest request, StreamObserver<CartResponse> responseObserver){
        CartItem newItem = new CartItem();
        newItem.setBookId(request.getBookId());
        newItem.setQuantity(request.getQuantity());
        Cart updatedcart = cartService.addItemToCart(request.getUserId(), newItem);

        CartResponse response = CartResponse.newBuilder()
                .setUserId(updatedcart.getUserId())
                .addAllItems(updatedcart.getItems().stream().map(this::mapToProtoItem).collect(Collectors.toList()))
                .setTotalPrice(updatedcart.calculateTotalPrice())
                .build();
        
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    @Override
    @Transactional
    public void clearCart(ClearCartRequest request, StreamObserver<CartResponse> responseObserver){
        cartService.clearCart(request.getUserId());
        Cart emptyCart = cartService.getCartByUserId(request.getUserId());

        CartResponse response = CartResponse.newBuilder()
                .setUserId(emptyCart.getUserId())
                .addAllItems(emptyCart.getItems().stream().map(this::mapToProtoItem).collect(Collectors.toList()))
                .setTotalPrice(emptyCart.getTotalPrice())
                .build();
        
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    // Método auxiliar para convertir entidad -> proto
    private com.bookstore.cart.grpc.CartItem mapToProtoItem(com.bookstore.cart_service.model.CartItem item) {
        com.bookstore.cart.grpc.CartItem.Builder builder = com.bookstore.cart.grpc.CartItem.newBuilder();
        if (item.getBookId() != null) builder.setBookId(item.getBookId());
        if (item.getTitle() != null) builder.setTitle(item.getTitle());
        if (item.getAuthor() != null) builder.setAuthor(item.getAuthor());
        if (item.getPrice() != null) builder.setPrice(item.getPrice());
        builder.setQuantity(item.getQuantity());
        
        return builder.build();
    }    
}