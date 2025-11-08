package com.bookstore.catalog.controller;

import com.bookstore.catalog.model.Book;
import com.bookstore.catalog.repository.BookRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/books")
public class BookController {

    private final BookRepository bookRepository;

    public BookController(BookRepository bookRepository){
        this.bookRepository = bookRepository;
    }

    // Obtener todos los libros
    @GetMapping
    public List<Book> getAllBooks(){
        return bookRepository.findAll();
    }


    // Obtener un libro por ID
    @GetMapping("/{id}")
    public ResponseEntity<Book> getBookById(@PathVariable Long id){
        return bookRepository.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // Crear un nuevo libro
    @PostMapping
    public ResponseEntity<Book> createBook(@RequestBody Book book){
        Book saved = bookRepository.save(book);
        return ResponseEntity.ok(saved);
    }

    // Actualizar un libro existente
    @PutMapping("/{id}")
    public ResponseEntity<Book> updateBook(@PathVariable Long id, @RequestBody Book updatedBook){
        return bookRepository.findById(id)
                .map(existingBook -> {
                    existingBook.setTitle(updatedBook.getTitle());
                    existingBook.setAuthor(updatedBook.getAuthor());
                    existingBook.setDescription(updatedBook.getDescription());
                    existingBook.setGenre(updatedBook.getGenre());
                    existingBook.setPrice(updatedBook.getPrice());
                    existingBook.setStock(updatedBook.getStock());
                    Book saved = bookRepository.save(existingBook);
                    return ResponseEntity.ok(saved);
                })
                .orElse(ResponseEntity.notFound().build());
    }

    // Eliminar un libro
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteBook(@PathVariable Long id){
        if (bookRepository.existsById(id)){
            bookRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // Disminuir stock de un libro
    @PutMapping("/{id}/decreaseStock")
    public ResponseEntity<String> decreaseStock(@PathVariable Long id, @RequestParam int quantity){
        Book book = bookRepository.findById(id).orElseThrow(() -> new RuntimeException("Libro no encontrado con ID: " + id));

        if (book.getStock() < quantity){
            return ResponseEntity.badRequest().body("Stock insuficiente para el libro: " + book.getTitle());
        }
        
        book.setStock(book.getStock() - quantity);
        bookRepository.save(book);

        return ResponseEntity.ok("Stock actualizado correctamente para el libro: " + book.getTitle());
    }
}