import { useState, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { getProducts, deleteProduct } from '@/services/products'
import { getCategories } from '@/services/categories'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { Select } from '@/components/ui/input'
import { LoadingSpinner, EmptyState, ErrorMessage } from '@/components/shared'
import { formatCurrency, isLowStock } from '@/lib/utils'
import { Plus, Search, Pencil, Trash2, AlertTriangle } from 'lucide-react'
import type { Product } from '@/types'

export function ProductsPage() {
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const [search, setSearch] = useState('')
    const [categoryId, setCategoryId] = useState('')
    const [debouncedSearch, setDebouncedSearch] = useState('')

    const handleSearch = useCallback((value: string) => {
        setSearch(value)
        clearTimeout((handleSearch as any)._t)
            ; (handleSearch as any)._t = setTimeout(() => setDebouncedSearch(value), 400)
    }, [])

    const { data: products, isLoading, error } = useQuery({
        queryKey: ['products', debouncedSearch, categoryId],
        queryFn: () => getProducts({ search: debouncedSearch || undefined, category_id: categoryId || undefined }),
    })

    const { data: categories } = useQuery({
        queryKey: ['categories'],
        queryFn: getCategories,
    })

    const deleteMutation = useMutation({
        mutationFn: deleteProduct,
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['products'] }),
    })

    const handleDelete = (product: Product) => {
        if (confirm(`Excluir "${product.name}"?`)) {
            deleteMutation.mutate(product.id)
        }
    }

    const categoryMap = Object.fromEntries((categories ?? []).map(c => [c.id, c.name]))

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Produtos</h1>
                    <p className="text-sm text-gray-500 mt-1">
                        {products?.length ?? 0} produto{(products?.length ?? 0) !== 1 ? 's' : ''} encontrado{(products?.length ?? 0) !== 1 ? 's' : ''}
                    </p>
                </div>
                <Button onClick={() => navigate('/products/new')}>
                    <Plus size={16} />
                    Novo Produto
                </Button>
            </div>

            <div className="flex gap-3">
                <div className="relative flex-1 max-w-sm">
                    <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <Input
                        placeholder="Buscar por nome..."
                        className="pl-9"
                        value={search}
                        onChange={(e) => handleSearch(e.target.value)}
                    />
                </div>
                <Select
                    className="w-48"
                    value={categoryId}
                    onChange={(e) => setCategoryId(e.target.value)}
                >
                    <option value="">Todas as categorias</option>
                    {categories?.map(c => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                </Select>
            </div>

            {error && <ErrorMessage />}

            {isLoading ? (
                <LoadingSpinner />
            ) : !products?.length ? (
                <EmptyState message="Nenhum produto encontrado. Crie o primeiro!" />
            ) : (
                <Card>
                    <CardContent className="p-0">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-100">
                                    <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wider px-6 py-4">Produto</th>
                                    <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wider px-6 py-4">Categoria</th>
                                    <th className="text-right text-xs font-semibold text-gray-500 uppercase tracking-wider px-6 py-4">Preço</th>
                                    <th className="text-center text-xs font-semibold text-gray-500 uppercase tracking-wider px-6 py-4">Estoque</th>
                                    <th className="px-6 py-4"></th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {products.map((product) => (
                                    <tr key={product.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4">
                                            <div>
                                                <p className="font-medium text-gray-900">{product.name}</p>
                                                {product.description && (
                                                    <p className="text-xs text-gray-400 mt-0.5 truncate max-w-xs">{product.description}</p>
                                                )}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            {product.category_id ? (
                                                <Badge variant="secondary">{categoryMap[product.category_id] ?? '—'}</Badge>
                                            ) : (
                                                <span className="text-sm text-gray-400">—</span>
                                            )}
                                        </td>
                                        <td className="px-6 py-4 text-right font-medium text-gray-900">
                                            {formatCurrency(product.price)}
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <div className="flex items-center justify-center gap-1.5">
                                                {isLowStock(product.stock) && (
                                                    <AlertTriangle size={14} className="text-amber-500" />
                                                )}
                                                <Badge variant={product.stock === 0 ? 'destructive' : isLowStock(product.stock) ? 'warning' : 'success'}>
                                                    {product.stock} un.
                                                </Badge>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => navigate(`/products/${product.id}/edit`)}
                                                >
                                                    <Pencil size={15} />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="text-red-500 hover:text-red-700 hover:bg-red-50"
                                                    onClick={() => handleDelete(product)}
                                                >
                                                    <Trash2 size={15} />
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </CardContent>
                </Card>
            )}
        </div>
    )
}
