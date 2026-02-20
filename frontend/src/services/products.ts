import api from './api'
import type { Product, ProductCreate, ProductUpdate } from '@/types'

export interface ProductsParams {
    skip?: number
    limit?: number
    search?: string
    category_id?: string
}

export const getProducts = async (params?: ProductsParams): Promise<Product[]> => {
    const { data } = await api.get('/products/', { params })
    return data
}

export const getProduct = async (id: string): Promise<Product> => {
    const { data } = await api.get(`/products/${id}`)
    return data
}

export const getLowStockProducts = async (): Promise<Product[]> => {
    const { data } = await api.get('/products/low-stock')
    return data
}

export const createProduct = async (product: ProductCreate): Promise<Product> => {
    const { data } = await api.post('/products/', product)
    return data
}

export const updateProduct = async (id: string, product: ProductUpdate): Promise<Product> => {
    const { data } = await api.patch(`/products/${id}`, product)
    return data
}

export const updateStock = async (id: string, stock: number): Promise<Product> => {
    const { data } = await api.patch(`/products/${id}/stock`, { stock })
    return data
}

export const deleteProduct = async (id: string): Promise<void> => {
    await api.delete(`/products/${id}`)
}
