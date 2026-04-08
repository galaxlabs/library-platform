import { LoginCard } from '../../../components/AuthCard';
import { defaultLocale, getTranslations } from '../../../lib/i18n';

export default function LoginPage() {
  return (
    <LoginCard
      locale={defaultLocale}
      copy={getTranslations(defaultLocale)}
    />
  );
}
