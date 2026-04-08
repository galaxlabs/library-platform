import { notFound } from 'next/navigation';

import { RegisterCard } from '../../../components/AuthCard';
import { defaultLocale, getTranslations, locales } from '../../../lib/i18n';

export default function LocalizedRegisterPage({
  params,
}: {
  params: { locale: string };
}) {
  const locale = params.locale;

  if (!locales.some((item) => item.code === locale) || locale === defaultLocale) {
    notFound();
  }

  return <RegisterCard locale={locale} copy={getTranslations(locale)} />;
}
