export interface UserProfile {
    userId: number;
    name: string;
    email: string;
    address: string;
    phone?: string; // Opcional
}

export type UserUpdateData = Partial<UserProfile>;