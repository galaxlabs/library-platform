'use client';

import Link from 'next/link';
import { ReactNode } from 'react';

import { useAuth } from '../contexts/AuthContext';

type PanelShellProps = {
  title: string;
  eyebrow: string;
  description: string;
  active: 'dashboard' | 'admin-panel' | 'chat' | 'library' | 'upload' | 'scholars' | 'institutes';
  children: ReactNode;
};

const links = [
  { href: '/', label: 'Home', key: null },
  { href: '/dashboard', label: 'User Dashboard', key: 'dashboard' },
  { href: '/library', label: 'Library', key: 'library' },
  { href: '/upload', label: 'Upload', key: 'upload' },
  { href: '/chat', label: 'Ask AI', key: 'chat' },
  { href: '/scholars', label: 'Scholar', key: 'scholars' },
  { href: '/institutes/my', label: 'Institute', key: 'institutes' },
  { href: '/admin-panel', label: 'Admin Panel', key: 'admin-panel' },
] as const;

export default function PanelShell({
  title,
  eyebrow,
  description,
  active,
  children,
}: PanelShellProps) {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <main className="app-shell min-h-screen px-4 py-4 md:px-8 md:py-6 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="panel-hero rounded-[2rem] p-5 md:p-6 lg:p-8">
          <div className="flex flex-col gap-8 xl:flex-row xl:items-end xl:justify-between">
            <div className="max-w-3xl">
              <p className="hero-kicker text-[11px] font-semibold text-[var(--accent)]">
                {eyebrow}
              </p>
              <h1 className="mt-3 text-4xl font-extrabold tracking-[-0.06em] text-slate-950 md:text-5xl">
                {title}
              </h1>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-600 md:text-base">
                {description}
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-[minmax(0,1fr)_auto] sm:items-end xl:min-w-[360px]">
              <div>
                <p className="hero-kicker text-[10px] font-semibold text-slate-500">
                  Workspace Switcher
                </p>
                <div className="mt-3 flex flex-wrap items-center gap-2 rounded-[1.6rem] border border-white/70 bg-white/60 p-2 shadow-[0_18px_40px_rgba(54,43,24,0.08)] backdrop-blur">
                  {links.map((link) => {
                    const isActive = link.key === active;
                    return (
                      <Link
                        key={link.href}
                        href={link.href}
                        className={`rounded-full px-4 py-2 text-xs font-semibold transition md:text-sm ${
                          isActive
                            ? 'bg-slate-950 text-white shadow-[0_14px_30px_rgba(15,23,42,0.22)]'
                            : 'text-slate-700 hover:bg-white'
                        }`}
                      >
                        {link.label}
                      </Link>
                    );
                  })}
                </div>
              </div>

              <div className="rounded-[1.5rem] border border-white/70 bg-white/65 px-4 py-4 text-right shadow-[0_18px_36px_rgba(54,43,24,0.08)] backdrop-blur sm:min-w-[200px]">
                <p className="hero-kicker text-[10px] font-semibold text-slate-500">
                  {isAuthenticated ? 'Signed In' : 'Surface'}
                </p>
                {isAuthenticated && user ? (
                  <>
                    <p className="mt-2 text-lg font-bold tracking-[-0.05em] text-slate-950">
                      {user.full_name}
                    </p>
                    <div className="mt-3 flex items-center justify-end gap-2">
                      <button
                        type="button"
                        onClick={logout}
                        className="rounded-full bg-slate-950 px-3 py-1.5 text-xs font-semibold text-white"
                      >
                        Logout
                      </button>
                    </div>
                  </>
                ) : (
                  <p className="mt-2 text-xl font-bold tracking-[-0.05em] text-slate-950">
                    {active === 'admin-panel' ? 'Control' : active === 'chat' ? 'Chat' : 'Study'}
                  </p>
                )}
              </div>
            </div>
          </div>
        </header>

        <section className="mt-6">{children}</section>
      </div>
    </main>
  );
}
