import { notFound } from 'next/navigation';

import HomePageContent from '../../components/HomePageContent';
import { defaultLocale, getTranslations, locales } from '../../lib/i18n';

export default function LocalizedHomePage({
  params,
}: {
  params: { locale: string };
}) {
  const locale = params.locale;

  if (!locales.some((item) => item.code === locale) || locale === defaultLocale) {
    notFound();
  }

  return <HomePageContent locale={locale} copy={getTranslations(locale)} />;
}
