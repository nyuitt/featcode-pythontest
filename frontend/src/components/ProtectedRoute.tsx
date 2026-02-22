import { useEffect, useRef } from 'react'
import { useKeycloak } from '@/context/KeycloakContext'
import { LoadingSpinner } from '@/components/shared'
import type { ReactNode } from 'react'

export function ProtectedRoute({ children }: { children: ReactNode }) {
    const { isAuthenticated, isLoading, login } = useKeycloak()
    // Prevent calling login() more than once per mount
    const loginCalled = useRef(false)

    useEffect(() => {
        if (!isLoading && !isAuthenticated && !loginCalled.current) {
            loginCalled.current = true
            login()
        }
    }, [isLoading, isAuthenticated, login])

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <LoadingSpinner />
            </div>
        )
    }

    if (!isAuthenticated) {
        // Render spinner while waiting for the redirect to happen
        return (
            <div className="flex items-center justify-center min-h-screen">
                <LoadingSpinner />
            </div>
        )
    }

    return <>{children}</>
}
