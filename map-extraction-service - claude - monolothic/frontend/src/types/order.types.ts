export interface Order {
    id: string;
    userId: string;
    area: number; // in square meters
    price: number; // total price for the order
    createdAt: Date;
    updatedAt: Date;
}

export interface OrderHistory {
    orders: Order[];
    totalOrders: number;
    totalPrice: number; // total price for all orders
}

export interface OrderRequest {
    area: number; // in square meters
}