import { cn } from '@/lib/utils'
import { cva, type VariantProps } from 'class-variance-authority'
import * as React from 'react'

const badgeVariants = cva(
    'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors',
    {
        variants: {
            variant: {
                default: 'bg-blue-100 text-blue-700',
                success: 'bg-green-100 text-green-700',
                warning: 'bg-amber-100 text-amber-700',
                destructive: 'bg-red-100 text-red-700',
                secondary: 'bg-gray-100 text-gray-700',
            },
        },
        defaultVariants: { variant: 'default' },
    }
)

export interface BadgeProps
    extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> { }

export function Badge({ className, variant, ...props }: BadgeProps) {
    return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}
