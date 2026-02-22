import axios from 'axios'
import keycloak from '@/lib/keycloak'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/api',
    headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
    if (keycloak.token) {
        config.headers.Authorization = `Bearer ${keycloak.token}`
    }
    return config
})

export default api
