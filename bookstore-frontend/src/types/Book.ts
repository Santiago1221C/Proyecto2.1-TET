export interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  genre?: string[];
  price: number;
  stock: number;
}