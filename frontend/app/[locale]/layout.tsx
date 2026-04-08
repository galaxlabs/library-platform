import { ReactNode } from 'react';
import { notFound } from 'next/navigation';

import { getLocaleDefinition, locales } from '../../lib/i18n';

export function generateStaticParams() {
  return locales
    .filter((locale) => locale.code !== 'en')
    .map((locale) => ({ locale: locale.code }));
}

export default function LocaleLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: { locale: string };
}) {
  const locale = locales.find((item) => item.code === params.locale);

  if (!locale || locale.code === 'en') {
    notFound();
  }

  const definition = getLocaleDefinition(params.locale);

  return (
    <div lang={definition.code} dir={definition.dir}>
      {children}
    </div>
  );
}
