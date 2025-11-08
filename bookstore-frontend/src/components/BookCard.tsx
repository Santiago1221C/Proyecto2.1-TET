import React from "react";
import type { Book } from "../types/Book";

interface Props {
    book: Book;
    onAddToCart: (book: Book) => void;
}

const BookCard: React.FC<Props> = ({ book, onAddToCart}) => (
    <div className="bg-white p-4 rounded shadow-md">
        <h2 className="text-lg font-bold mb-1">{book.title}</h2>
        <p className="text-sm text-gray-600">by {book.author}</p>
        <p className="mt-2 text-gray-800">{book.description}</p>
        <p className="mt-2 font-bold">${book.price.toFixed(2)}</p>
        <button
            onClick={() => onAddToCart(book)}
            className="mt-4 bg-blue-600 text-white py-1 px-3 rounded hover:bg-blue-700"
        >
            Añadir al carrito       
        </button>
    </div>
);

export default BookCard;