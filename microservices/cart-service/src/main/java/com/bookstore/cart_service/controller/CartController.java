package com.bookstore.cart_service.controller;

import com.bookstore.cart_service.model.Cart;
import com.bookstore.cart_service.model.CartItem;
import com.bookstore.cart_service.service.CartService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/cart")
public class CartController {

    private final CartService cartService;

    public CartController(CartService cartService) {
        this.cartService = cartService;
    }

    // Crear un carrito nuevo para un usuario
    @PostMapping("/create/{userId}")
    public ResponseEntity<Cart> createCart(@PathVariable Long userId){
        Cart cart = cartService.createCart(userId);
        return ResponseEntity.ok(cart);
    }

    // Agrega un libro al carrito del usuario, consultando primero el stock al servicio de catálogo por gRPC
    @PostMapping("/{userId}/add")
    public ResponseEntity<Cart> addItemToCart(@PathVariable Long userId, @RequestBody CartItem item) {
        try {
            Cart updatedCart = cartService.addItemToCart(userId, item);
            return ResponseEntity.ok(updatedCart);
        } catch (RuntimeException ex) {
            return ResponseEntity.badRequest().body(null);
        }
    }

    // Obtiene el carrito actual del usuario
    @GetMapping("/{userId}")
    public ResponseEntity<Cart> getCartByUser(@PathVariable Long userId) {
        try {
            Cart cart = cartService.getCartByUserId(userId);
            return ResponseEntity.ok(cart);
        } catch (RuntimeException ex) {
            return ResponseEntity.notFound().build();
        }
    }


    // Elimina un libro del carrito del usuario
    @DeleteMapping("/{userId}/remove/{bookId}")
    public ResponseEntity<String> removeItem(@PathVariable Long userId, @PathVariable Long bookId){
        try {
            cartService.removeItem(userId, bookId);
            return ResponseEntity.ok("Libro eliminado del carrito correctamente.");
        } catch (RuntimeException ex) {
            return ResponseEntity.badRequest().body("Error: " + ex.getMessage());
        }
    }

    // Vacía completamente el carrito del usuario
    @DeleteMapping("/{userId}")
    public ResponseEntity<String> clearCart(@PathVariable Long userId){
        try {
            cartService.clearCart(userId);
            return ResponseEntity.ok("Carrito vaciado correctamente.");
        } catch (RuntimeException ex) {
            return ResponseEntity.badRequest().body("Error: " + ex.getMessage());
        }
    }

    // Eliminar completamente el carrito
    @DeleteMapping("{userId}/delete")
    public ResponseEntity<String> deleteCart(@PathVariable Long userId){
        cartService.deleteCart(userId);
        return ResponseEntity.ok("Carrito eliminado por el usuario con ID: " + userId);
    }
}