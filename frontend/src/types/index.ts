export interface Category {
    id: string
    name: string
    description: string | null
}

export interface Product {
    id: string
    name: string
    description: string | null
    price: number
    stock: number
    category_id: string | null
}

export interface ProductCreate {
    name: string
    description?: string
    price: number
    stock: number
    category_id?: string
}

export interface ProductUpdate {
    name?: string
    description?: string
    price?: number
    stock?: number
    category_id?: string
}

export interface CategoryCreate {
    name: string
    description?: string
}

export interface CategorySummary {
    category_id: string | null
    category_name: string | null
    product_count: number
}

export interface ProductLowStock {
    id: string
    name: string
    stock: number
    category_id: string | null
}

export interface DashboardData {
    total_products: number
    total_categories: number
    total_stock_value: number
    low_stock_count: number
    low_stock_products: ProductLowStock[]
    products_by_category: CategorySummary[]
}
