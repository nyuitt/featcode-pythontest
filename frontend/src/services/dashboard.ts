import api from './api'
import type { DashboardData } from '@/types'

export const getDashboard = async (): Promise<DashboardData> => {
    const { data } = await api.get('/dashboard/')
    return data
}
