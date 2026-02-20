import api from './api'
import type { Category, CategoryCreate } from '@/types'

export const getCategories = async (): Promise<Category[]> => {
    const { data } = await api.get('/categories/')
    return data
}

export const createCategory = async (category: CategoryCreate): Promise<Category> => {
    const { data } = await api.post('/categories/', category)
    return data
}

export const updateCategory = async (id: string, category: Partial<CategoryCreate>): Promise<Category> => {
    const { data } = await api.patch(`/categories/${id}`, category)
    return data
}

export const deleteCategory = async (id: string): Promise<void> => {
    await api.delete(`/categories/${id}`)
}
