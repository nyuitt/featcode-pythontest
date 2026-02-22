import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import keycloak from '@/lib/keycloak'

interface KeycloakContextValue {
    isAuthenticated: boolean
    isLoading: boolean
    token: string | undefined
    userEmail: string | undefined
    userName: string | undefined
    login: () => void
    logout: () => void
}

const KeycloakContext = createContext<KeycloakContextValue | null>(null)

// Module-level flag: guarantees init() is called only once even in React StrictMode
let initStarted = false

export function KeycloakProvider({ children }: { children: ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        if (initStarted) return
        initStarted = true

        keycloak
            .init({
                onLoad: 'check-sso',
                silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
                pkceMethod: 'S256',
                // Ensures the callback URL params are consumed and cleared
                checkLoginIframe: false,
            })
            .then((authenticated) => {
                setIsAuthenticated(authenticated)
                setIsLoading(false)

                if (authenticated) {
                    scheduleTokenRefresh()
                }
            })
            .catch(() => {
                setIsLoading(false)
            })
    }, [])

    function scheduleTokenRefresh() {
        setInterval(() => {
            keycloak.updateToken(60).catch(() => {
                keycloak.login()
            })
        }, 30_000)
    }

    return (
        <KeycloakContext.Provider
            value={{
                isAuthenticated,
                isLoading,
                token: keycloak.token,
                userEmail: keycloak.tokenParsed?.email,
                userName: keycloak.tokenParsed?.name ?? keycloak.tokenParsed?.preferred_username,
                login: () => keycloak.login(),
                logout: () => keycloak.logout({ redirectUri: window.location.origin }),
            }}
        >
            {children}
        </KeycloakContext.Provider>
    )
}

export function useKeycloak() {
    const ctx = useContext(KeycloakContext)
    if (!ctx) throw new Error('useKeycloak must be used inside KeycloakProvider')
    return ctx
}
