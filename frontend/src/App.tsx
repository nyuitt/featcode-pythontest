import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { KeycloakProvider } from '@/context/KeycloakContext'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { AppLayout } from '@/components/layout/AppLayout'
import { DashboardPage } from '@/pages/DashboardPage'
import { ProductsPage } from '@/pages/ProductsPage'
import { ProductFormPage } from '@/pages/ProductFormPage'
import { CategoriesPage } from '@/pages/CategoriesPage'

function App() {
  return (
    <BrowserRouter>
      <KeycloakProvider>
        <Routes>
          <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/products/new" element={<ProductFormPage />} />
            <Route path="/products/:id/edit" element={<ProductFormPage />} />
            <Route path="/categories" element={<CategoriesPage />} />
          </Route>
        </Routes>
      </KeycloakProvider>
    </BrowserRouter>
  )
}

export default App
