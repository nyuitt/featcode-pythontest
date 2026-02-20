import { useQuery } from '@tanstack/react-query'
import { getDashboard } from '@/services/dashboard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { LoadingSpinner, ErrorMessage } from '@/components/shared'
import { formatCurrency } from '@/lib/utils'
import { Package, DollarSign, AlertTriangle, Tag } from 'lucide-react'
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts'

export function DashboardPage() {
    const { data, isLoading, error } = useQuery({
        queryKey: ['dashboard'],
        queryFn: getDashboard,
        refetchInterval: 30000,
    })

    if (isLoading) return <LoadingSpinner />
    if (error) return <ErrorMessage message="Erro ao carregar dashboard." />

    const stats = [
        {
            title: 'Total de Produtos',
            value: data?.total_products ?? 0,
            icon: Package,
            color: 'text-blue-600',
            bg: 'bg-blue-50',
        },
        {
            title: 'Valor do Estoque',
            value: formatCurrency(Number(data?.total_stock_value ?? 0)),
            icon: DollarSign,
            color: 'text-green-600',
            bg: 'bg-green-50',
        },
        {
            title: 'Estoque Crítico',
            value: data?.low_stock_count ?? 0,
            icon: AlertTriangle,
            color: 'text-amber-600',
            bg: 'bg-amber-50',
        },
        {
            title: 'Categorias',
            value: data?.total_categories ?? 0,
            icon: Tag,
            color: 'text-purple-600',
            bg: 'bg-purple-50',
        },
    ]

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-sm text-gray-500 mt-1">Visão geral do sistema de gestão</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
                {stats.map(({ title, value, icon: Icon, color, bg }) => (
                    <Card key={title}>
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm text-gray-500 font-medium">{title}</p>
                                    <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
                                </div>
                                <div className={`w-12 h-12 rounded-xl ${bg} flex items-center justify-center`}>
                                    <Icon size={22} className={color} />
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Produtos por Categoria</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {data?.products_by_category && data.products_by_category.length > 0 ? (
                            <ResponsiveContainer width="100%" height={260}>
                                <BarChart data={data.products_by_category} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis
                                        dataKey="category_name"
                                        tick={{ fontSize: 12, fill: '#6b7280' }}
                                        tickLine={false}
                                        axisLine={false}
                                    />
                                    <YAxis
                                        tick={{ fontSize: 12, fill: '#6b7280' }}
                                        tickLine={false}
                                        axisLine={false}
                                        allowDecimals={false}
                                    />
                                    <Tooltip
                                        contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                                        formatter={(value) => [`${value} produtos`, 'Quantidade']}
                                    />
                                    <Bar dataKey="product_count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        ) : (
                            <p className="text-sm text-gray-400 text-center py-16">Nenhum produto cadastrado.</p>
                        )}
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <AlertTriangle size={16} className="text-amber-500" />
                            Estoque Crítico
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {data?.low_stock_products && data.low_stock_products.length > 0 ? (
                            <div className="space-y-3">
                                {data.low_stock_products.slice(0, 6).map((p) => (
                                    <div key={p.id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                                        <span className="text-sm font-medium text-gray-700 truncate flex-1 mr-3">{p.name}</span>
                                        <Badge variant={p.stock === 0 ? 'destructive' : 'warning'}>
                                            {p.stock} un.
                                        </Badge>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-sm text-gray-400 text-center py-10">✓ Todos os produtos com estoque adequado</p>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
