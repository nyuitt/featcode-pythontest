import { cn } from '@/lib/utils'
import * as React from 'react'

interface DialogProps {
    open: boolean
    onClose: () => void
    children: React.ReactNode
    className?: string
}

export function Dialog({ open, onClose, children }: DialogProps) {
    React.useEffect(() => {
        const handleKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
        if (open) document.addEventListener('keydown', handleKey)
        return () => document.removeEventListener('keydown', handleKey)
    }, [open, onClose])

    if (!open) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
            <div className="relative z-10 w-full max-w-lg mx-4">
                {children}
            </div>
        </div>
    )
}

export function DialogContent({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div className={cn('rounded-xl bg-white shadow-xl p-6 space-y-4', className)} {...props}>
            {children}
        </div>
    )
}

export function DialogHeader({ children }: { children: React.ReactNode }) {
    return <div className="space-y-1">{children}</div>
}

export function DialogTitle({ children }: { children: React.ReactNode }) {
    return <h2 className="text-lg font-semibold text-gray-900">{children}</h2>
}

export function DialogFooter({ children }: { children: React.ReactNode }) {
    return <div className="flex justify-end gap-3 pt-2">{children}</div>
}
