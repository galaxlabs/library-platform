'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';

import { useAuth } from '../contexts/AuthContext';

export default function RequireAuth({ children }: { children: ReactNode }) {
  const { loading, isAuthenticated } = useAuth();
  const pathname = usePathname();

  if (loading) {
    return (
      <div className="rounded-[1.6rem] border border-slate-200 bg-white/85 p-6 text-sm text-slate-600">
        Loading your workspace...
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="rounded-[1.8rem] border border-amber-200 bg-amber-50 p-6">
        <p className="text-sm font-semibold text-amber-900">Sign in required</p>
        <p className="mt-3 text-sm leading-7 text-amber-800">
          This page is part of your private learning workspace and needs an authenticated session.
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <Link
            href={`/login?next=${encodeURIComponent(pathname || '/dashboard')}`}
            className="rounded-[1rem] bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white"
          >
            Go to login
          </Link>
          <Link
            href="/register"
            className="rounded-[1rem] bg-white px-4 py-2.5 text-sm font-semibold text-slate-900 ring-1 ring-slate-200"
          >
            Create account
          </Link>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
