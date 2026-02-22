import { cn } from '@/lib/utils'
import { LayoutDashboard, Package, Tag, ChevronRight, LogOut, User } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { useKeycloak } from '@/context/KeycloakContext'

const navItems = [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/products', icon: Package, label: 'Produtos' },
    { to: '/categories', icon: Tag, label: 'Categorias' },
]

export function Sidebar() {
    const { userName, userEmail, logout } = useKeycloak()

    return (
        <aside className="fixed left-0 top-0 h-full w-64 bg-slate-900 flex flex-col z-40">
            <div className="flex items-center gap-3 px-6 py-5 border-b border-slate-800">
                <div className="w-8 h-8 rounded-lg bg-blue-500 flex items-center justify-center">
                    <Package size={18} className="text-white" />
                </div>
                <span className="font-bold text-white text-lg">Featcode</span>
            </div>

            <nav className="flex-1 px-3 py-4 space-y-1">
                {navItems.map(({ to, icon: Icon, label }) => (
                    <NavLink
                        key={to}
                        to={to}
                        end={to === '/'}
                        className={({ isActive }) =>
                            cn(
                                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group',
                                isActive
                                    ? 'bg-blue-600 text-white'
                                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                            )
                        }
                    >
                        {({ isActive }) => (
                            <>
                                <Icon size={18} />
                                <span className="flex-1">{label}</span>
                                {isActive && <ChevronRight size={14} />}
                            </>
                        )}
                    </NavLink>
                ))}
            </nav>

            <div className="px-3 py-4 border-t border-slate-800 space-y-3">
                {/* User info */}
                <div className="flex items-center gap-3 px-3">
                    <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0">
                        <User size={16} className="text-slate-300" />
                    </div>
                    <div className="min-w-0">
                        <p className="text-sm font-medium text-white truncate">
                            {userName ?? 'Usuário'}
                        </p>
                        {userEmail && (
                            <p className="text-xs text-slate-500 truncate">{userEmail}</p>
                        )}
                    </div>
                </div>

                {/* Logout button */}
                <button
                    onClick={logout}
                    className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:bg-red-900/40 hover:text-red-400 transition-all duration-150"
                >
                    <LogOut size={18} />
                    <span>Sair</span>
                </button>
            </div>
        </aside>
    )
}
