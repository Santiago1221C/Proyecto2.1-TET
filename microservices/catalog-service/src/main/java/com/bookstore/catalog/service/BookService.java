package com.bookstore.catalog.service;

import com.bookstore.catalog.model.Book;
import com.bookstore.catalog.repository.BookRepository;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class BookService {
    
    private final BookRepository repository;

    public BookService(BookRepository repository){
        this.repository = repository;
    }

    public List<Book> getAllBooks(){
        return repository.findAll();
    }

    public Optional<Book> getBookById(Long id){
        return repository.findById(id);
    }

    public Book createBook(Book book){
        return repository.save(book);
    }

    public Book updateBook(Long id, Book book){
        book.setId(id);
        return repository.save(book);
    }

    public void deleteBook(Long id){
        repository.deleteById(id);
    }

    public List<Book> searchByTitle(String title){
        return repository.findByTitleContainingIgnoreCase(title);
    }

    public List<Book> searchByAuthor(String author){
        return repository.findByAuthorContainingIgnoreCase(author);
    }

    public List<Book> searchByGenre(String genre){
        return repository.findByGenreContainingIgnoreCase(genre);
    }
}