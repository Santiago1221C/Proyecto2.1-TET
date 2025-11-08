export interface Order {
    id: number;
    userId: number;
    items: {
        bookId: number;
        title: string;
        author: string;
        price: number;
        quantity : number;
    }[];
    totalPrice: number;
    status: string;
    createdAt: string;
}