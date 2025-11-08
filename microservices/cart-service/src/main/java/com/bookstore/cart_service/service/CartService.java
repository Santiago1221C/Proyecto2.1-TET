package com.bookstore.cart_service.service;

import com.bookstore.cart_service.grpc.CatalogGrpcClient;
import com.bookstore.cart_service.model.Cart;
import com.bookstore.cart_service.model.CartItem;
import com.bookstore.cart_service.repository.CartRepository;
import com.bookstore.catalog.grpc.BookResponse;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CartService {

    private final CartRepository cartRepository;
    private final CatalogGrpcClient catalogGrpcClient;

    public CartService(CartRepository cartRepository, CatalogGrpcClient catalogGrpcClient) {
        this.cartRepository = cartRepository;
        this.catalogGrpcClient = catalogGrpcClient;
    }

    public Cart createCart(Long userId) {
        return cartRepository.findByUserId(userId)
                .orElseGet(() -> cartRepository.save(new Cart(userId)));
    }

    @Transactional
    public Cart addItemToCart(Long userId, CartItem newItem) {
        System.out.println("[CartService] Intentando agregar el libro con ID " + newItem.getBookId() + " al carrito del usuario " + userId);
        
        // Busca carrito existente o lo crea si no existe
        Cart cart = cartRepository.findByUserId(userId)
                .orElseGet(() -> {
                    System.out.println("[CartService] No se encontró carrito. Creando uno nuevo...");
                    return cartRepository.save(new Cart(userId));
                });
        
        // Verificar stock por gRPC
        boolean stockAvailable = catalogGrpcClient.checkStock(newItem.getBookId(), newItem.getQuantity());


        if (!stockAvailable) {
            throw new RuntimeException("No hay suficiente stock para el libro con ID " + newItem.getBookId());
        }

        // Consultar información completa del libro
        BookResponse bookInfo = catalogGrpcClient.getBookById(newItem.getBookId());

        // Verificar si el item ya existe en el carrito (sumar cantidades)
        Optional<CartItem> existingItemOpt = cart.getItems().stream()
                .filter(i -> i.getBookId().equals(newItem.getBookId()))
                .findFirst();
        
        if (existingItemOpt.isPresent()) {
            CartItem existingItem = existingItemOpt.get();
            existingItem.setQuantity(existingItem.getQuantity() + newItem.getQuantity());
            System.out.println("[CartService] Libro ya estaba en el carrito. Nueva cantidad: " + existingItem.getQuantity());
        } else {
            newItem.setTitle(bookInfo.getTitle());
            newItem.setAuthor(bookInfo.getAuthor());
            newItem.setPrice(bookInfo.getPrice());
            newItem.setCart(cart);
            cart.getItems().add(newItem);
            System.out.println("[CartService] Libro agregado al carrito con datos completos: " + newItem.getTitle());
        }

        return cartRepository.save(cart);
    }


    @Transactional
    public void clearCart(Long userId){
        Cart cart = getCartByUserId(userId);
        cart.getItems().clear();
        cartRepository.save(cart);
        System.out.println("[CartService] Carrito vaciado correctamente");
    }

    @Transactional
    public Cart getCartByUserId(Long userId) {
        return cartRepository.findByUserId(userId).orElseThrow(() -> new RuntimeException("Carrito no encontrado para el usuario: " + userId));
    }

    @Transactional
    public void removeItem(Long userId, Long bookId) {
        Cart cart = getCartByUserId(userId);
        cart.getItems().removeIf(item -> item.getBookId().equals(bookId));
        cartRepository.save(cart);
        System.out.println("[CartService] Item removido del carrito: " + bookId);
    }

    // Eliminar carrito completamente
    @Transactional
    public void deleteCart(Long userId){
        Cart cart = getCartByUserId(userId);
        cartRepository.delete(cart);
        System.out.println("[CartService] Carrito eliminado por completo");
    }
}