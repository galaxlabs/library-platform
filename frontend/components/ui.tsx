'use client';

import { ReactNode } from 'react';

export function SurfaceCard({
  title,
  eyebrow,
  children,
}: {
  title: string;
  eyebrow?: string;
  children: ReactNode;
}) {
  return (
    <section className="rounded-[1.8rem] border border-slate-200 bg-white/90 p-5 shadow-[0_18px_40px_rgba(40,39,33,0.08)]">
      {eyebrow ? (
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">{eyebrow}</p>
      ) : null}
      <h2 className="mt-2 text-2xl font-bold tracking-[-0.04em] text-slate-950">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

export function StatusBadge({
  children,
  tone = 'neutral',
}: {
  children: ReactNode;
  tone?: 'neutral' | 'success' | 'warning' | 'danger';
}) {
  const tones = {
    neutral: 'bg-slate-100 text-slate-700',
    success: 'bg-emerald-50 text-emerald-800',
    warning: 'bg-amber-50 text-amber-900',
    danger: 'bg-red-50 text-red-700',
  };

  return (
    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${tones[tone]}`}>
      {children}
    </span>
  );
}
