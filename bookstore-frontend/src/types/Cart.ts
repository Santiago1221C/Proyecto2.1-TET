export interface CartItem {
    bookId: number;
    title: string;
    author: string;
    price: number;
    quantity: number;
}

export interface Cart {
    userId: number;
    items: CartItem[];
    totalPrice: number;
}