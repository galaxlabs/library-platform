import HomePageContent from '../components/HomePageContent';
import { defaultLocale, getTranslations } from '../lib/i18n';

export default function HomePage() {
  return (
    <HomePageContent
      locale={defaultLocale}
      copy={getTranslations(defaultLocale)}
    />
  );
}
