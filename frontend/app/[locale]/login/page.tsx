import { notFound } from 'next/navigation';

import { LoginCard } from '../../../components/AuthCard';
import { defaultLocale, getTranslations, locales } from '../../../lib/i18n';

export default function LocalizedLoginPage({
  params,
}: {
  params: { locale: string };
}) {
  const locale = params.locale;

  if (!locales.some((item) => item.code === locale) || locale === defaultLocale) {
    notFound();
  }

  return <LoginCard locale={locale} copy={getTranslations(locale)} />;
}
