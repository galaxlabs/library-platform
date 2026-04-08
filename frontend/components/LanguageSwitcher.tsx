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
    <div className="flex flex-wrap items-center gap-2">
      <span className="text-xs font-medium uppercase tracking-[0.2em] text-slate-400">
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
            className={`rounded-full border px-3 py-1 text-xs font-medium transition ${
              active
                ? 'border-emerald-400 bg-emerald-400/10 text-emerald-300'
                : 'border-white/10 bg-white/5 text-slate-300 hover:bg-white/10'
            }`}
          >
            {locale.nativeLabel}
          </Link>
        );
      })}
    </div>
  );
}
