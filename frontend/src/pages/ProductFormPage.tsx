import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { getProduct, createProduct, updateProduct } from '@/services/products'
import { getCategories } from '@/services/categories'
import { Button } from '@/components/ui/button'
import { Input, Textarea, Label, Select } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner, ErrorMessage } from '@/components/shared'
import { ArrowLeft } from 'lucide-react'

const schema = z.object({
    name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
    description: z.string().optional(),
    price: z.coerce.number({ invalid_type_error: 'Preço inválido' }).positive('Preço deve ser maior que 0'),
    stock: z.coerce.number({ invalid_type_error: 'Estoque inválido' }).int().min(0, 'Estoque não pode ser negativo'),
    category_id: z.string().optional(),
})

type FormData = z.infer<typeof schema>

export function ProductFormPage() {
    const { id } = useParams()
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const isEditing = Boolean(id)

    const { data: product, isLoading: loadingProduct } = useQuery({
        queryKey: ['product', id],
        queryFn: () => getProduct(id!),
        enabled: isEditing,
    })

    const { data: categories } = useQuery({
        queryKey: ['categories'],
        queryFn: getCategories,
    })

    const { register, handleSubmit, reset, control, formState: { errors, isSubmitting } } = useForm<FormData>({
        resolver: zodResolver(schema),
    })

    useEffect(() => {
        if (product) {
            reset({
                name: product.name,
                description: product.description ?? '',
                price: product.price,
                stock: product.stock,
                category_id: product.category_id ?? '',
            })
        }
    }, [product, reset])

    const mutation = useMutation({
        mutationFn: (data: FormData) => {
            const payload = { ...data, category_id: data.category_id || undefined }
            return isEditing ? updateProduct(id!, payload) : createProduct(payload as any)
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['products'] })
            queryClient.invalidateQueries({ queryKey: ['dashboard'] })
            navigate('/products')
        },
    })

    if (isEditing && loadingProduct) return <LoadingSpinner />

    return (
        <div className="max-w-2xl">
            <div className="mb-6">
                <button
                    onClick={() => navigate('/products')}
                    className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 transition-colors mb-4"
                >
                    <ArrowLeft size={16} />
                    Voltar para Produtos
                </button>
                <h1 className="text-2xl font-bold text-gray-900">
                    {isEditing ? 'Editar Produto' : 'Novo Produto'}
                </h1>
            </div>

            <Card>
                <CardContent className="p-6">
                    <form onSubmit={handleSubmit((data) => mutation.mutate(data))} className="space-y-5">
                        <div className="space-y-1.5">
                            <Label htmlFor="name">Nome *</Label>
                            <Input id="name" placeholder="Ex: Notebook Dell XPS" {...register('name')} />
                            {errors.name && <p className="text-xs text-red-500">{errors.name.message}</p>}
                        </div>

                        <div className="space-y-1.5">
                            <Label htmlFor="description">Descrição</Label>
                            <Textarea id="description" placeholder="Descrição opcional do produto..." {...register('description')} />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1.5">
                                <Label htmlFor="price">Preço (R$) *</Label>
                                <Input
                                    id="price"
                                    type="number"
                                    step="0.01"
                                    min="0.01"
                                    placeholder="0,00"
                                    {...register('price')}
                                />
                                {errors.price && <p className="text-xs text-red-500">{errors.price.message}</p>}
                            </div>

                            <div className="space-y-1.5">
                                <Label htmlFor="stock">Estoque *</Label>
                                <Input
                                    id="stock"
                                    type="number"
                                    min="0"
                                    placeholder="0"
                                    {...register('stock')}
                                />
                                {errors.stock && <p className="text-xs text-red-500">{errors.stock.message}</p>}
                            </div>
                        </div>

                        <div className="space-y-1.5">
                            <Label htmlFor="category_id">Categoria</Label>
                            <Controller
                                name="category_id"
                                control={control}
                                render={({ field }) => (
                                    <Select id="category_id" {...field}>
                                        <option value="">Sem categoria</option>
                                        {categories?.map(c => (
                                            <option key={c.id} value={c.id}>{c.name}</option>
                                        ))}
                                    </Select>
                                )}
                            />
                        </div>

                        {mutation.error && <ErrorMessage message="Erro ao salvar produto. Tente novamente." />}

                        <div className="flex gap-3 pt-2">
                            <Button type="submit" disabled={isSubmitting || mutation.isPending}>
                                {mutation.isPending ? 'Salvando...' : isEditing ? 'Salvar alterações' : 'Criar produto'}
                            </Button>
                            <Button type="button" variant="outline" onClick={() => navigate('/products')}>
                                Cancelar
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
