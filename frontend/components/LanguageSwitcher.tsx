'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

import { defaultLocale, locales } from '../lib/i18n';

type LanguageSwitcherProps = {
  currentLocale?: string;
  label: string;
};

export default function LanguageSwitcher({
  currentLocale = defaultLocale,
  label,
}: LanguageSwitcherProps) {
  const pathname = usePathname() || '/';
  const normalizedPath = pathname === '/' ? '' : pathname;
  const suffix =
    currentLocale !== defaultLocale &&
    normalizedPath.startsWith(`/${currentLocale}`)
      ? normalizedPath.slice(currentLocale.length + 1)
      : normalizedPath;

  return (
    <div className="glass-panel inline-flex max-w-full flex-wrap items-center gap-2 rounded-[1.75rem] px-3 py-3">
      <span className="px-2 text-[11px] font-semibold uppercase tracking-[0.28em] text-slate-500">
        {label}
      </span>
      {locales.map((locale) => {
        const href =
          locale.code === defaultLocale
            ? suffix || '/'
            : `/${locale.code}${suffix || ''}`;

        const active = locale.code === currentLocale;

        return (
          <Link
            key={locale.code}
            href={href}
            className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
              active
                ? 'border-emerald-700/20 bg-emerald-900 text-emerald-50 shadow-lg shadow-emerald-950/15'
                : 'border-slate-300/70 bg-white/70 text-slate-600 hover:border-slate-400 hover:bg-white'
            }`}
          >
            {locale.nativeLabel}
          </Link>
        );
      })}
    </div>
  );
}
