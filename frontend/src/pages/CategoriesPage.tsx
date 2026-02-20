import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { getCategories, createCategory, deleteCategory } from '@/services/categories'
import { Button } from '@/components/ui/button'
import { Input, Textarea, Label } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { LoadingSpinner, EmptyState, ErrorMessage } from '@/components/shared'
import { Plus, Trash2, Tag } from 'lucide-react'

const schema = z.object({
    name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
    description: z.string().optional(),
})
type FormData = z.infer<typeof schema>

export function CategoriesPage() {
    const queryClient = useQueryClient()
    const [open, setOpen] = useState(false)

    const { data: categories, isLoading, error } = useQuery({
        queryKey: ['categories'],
        queryFn: getCategories,
    })

    const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<FormData>({
        resolver: zodResolver(schema),
    })

    const createMutation = useMutation({
        mutationFn: createCategory,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['categories'] })
            queryClient.invalidateQueries({ queryKey: ['dashboard'] })
            reset()
            setOpen(false)
        },
    })

    const deleteMutation = useMutation({
        mutationFn: deleteCategory,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['categories'] })
            queryClient.invalidateQueries({ queryKey: ['dashboard'] })
        },
    })

    const handleDelete = (id: string, name: string) => {
        if (confirm(`Excluir a categoria "${name}"? Os produtos vinculados ficarão sem categoria.`)) {
            deleteMutation.mutate(id)
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Categorias</h1>
                    <p className="text-sm text-gray-500 mt-1">
                        {categories?.length ?? 0} categoria{(categories?.length ?? 0) !== 1 ? 's' : ''} cadastrada{(categories?.length ?? 0) !== 1 ? 's' : ''}
                    </p>
                </div>
                <Button onClick={() => setOpen(true)}>
                    <Plus size={16} />
                    Nova Categoria
                </Button>
            </div>

            {error && <ErrorMessage />}

            {isLoading ? (
                <LoadingSpinner />
            ) : !categories?.length ? (
                <EmptyState message="Nenhuma categoria encontrada. Crie a primeira!" />
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {categories.map((category) => (
                        <Card key={category.id} className="hover:shadow-md transition-shadow">
                            <CardContent className="p-5">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center flex-shrink-0">
                                            <Tag size={18} className="text-blue-600" />
                                        </div>
                                        <div>
                                            <p className="font-semibold text-gray-900">{category.name}</p>
                                            {category.description && (
                                                <p className="text-xs text-gray-400 mt-0.5 line-clamp-2">{category.description}</p>
                                            )}
                                        </div>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="text-red-400 hover:text-red-600 hover:bg-red-50 ml-2 flex-shrink-0"
                                        onClick={() => handleDelete(category.id, category.name)}
                                    >
                                        <Trash2 size={15} />
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

            <Dialog open={open} onClose={() => { setOpen(false); reset() }}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Nova Categoria</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={handleSubmit((data) => createMutation.mutate(data))} className="space-y-4">
                        <div className="space-y-1.5">
                            <Label htmlFor="name">Nome *</Label>
                            <Input id="name" placeholder="Ex: Eletrônicos" {...register('name')} />
                            {errors.name && <p className="text-xs text-red-500">{errors.name.message}</p>}
                        </div>
                        <div className="space-y-1.5">
                            <Label htmlFor="description">Descrição</Label>
                            <Textarea id="description" placeholder="Opcional..." {...register('description')} />
                        </div>
                        {createMutation.error && <ErrorMessage message="Erro ao criar categoria." />}
                        <DialogFooter>
                            <Button type="button" variant="outline" onClick={() => { setOpen(false); reset() }}>
                                Cancelar
                            </Button>
                            <Button type="submit" disabled={isSubmitting || createMutation.isPending}>
                                {createMutation.isPending ? 'Criando...' : 'Criar'}
                            </Button>
                        </DialogFooter>
                    </form>
                </DialogContent>
            </Dialog>
        </div>
    )
}
