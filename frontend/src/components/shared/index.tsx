export function LoadingSpinner({ className }: { className?: string }) {
    return (
        <div className={`flex items-center justify-center py-12 ${className}`}>
            <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
        </div>
    )
}

export function EmptyState({ message = 'Nenhum item encontrado.' }: { message?: string }) {
    return (
        <div className="flex flex-col items-center justify-center py-16 text-gray-400">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
            </div>
            <p className="text-sm">{message}</p>
        </div>
    )
}

interface ErrorMessageProps { message?: string }
export function ErrorMessage({ message = 'Erro ao carregar dados.' }: ErrorMessageProps) {
    return (
        <div className="rounded-lg bg-red-50 border border-red-200 p-4 text-sm text-red-700">
            {message}
        </div>
    )
}
