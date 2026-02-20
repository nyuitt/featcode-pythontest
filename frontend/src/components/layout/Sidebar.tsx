import { cn } from '@/lib/utils'
import { LayoutDashboard, Package, Tag, ChevronRight } from 'lucide-react'
import { NavLink } from 'react-router-dom'

const navItems = [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/products', icon: Package, label: 'Produtos' },
    { to: '/categories', icon: Tag, label: 'Categorias' },
]

export function Sidebar() {
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

            <div className="px-6 py-4 border-t border-slate-800">
                <p className="text-xs text-slate-500">Gestão de Produtos v0.1</p>
            </div>
        </aside>
    )
}
