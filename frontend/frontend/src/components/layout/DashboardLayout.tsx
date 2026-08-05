import type { ReactNode } from "react";

interface DashboardLayoutProps {
    children: ReactNode;
}

export default function DashboardLayout({
    children,
}: DashboardLayoutProps) {
    return (
        <main className="min-h-screen bg-slate-100">
            <div className="mx-auto max-w-7xl p-8">
                {children}
            </div>
        </main>
    );
}