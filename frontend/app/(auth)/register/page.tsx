import { RegisterCard } from '../../../components/AuthCard';
import { defaultLocale, getTranslations } from '../../../lib/i18n';

export default function RegisterPage() {
  return (
    <RegisterCard
      locale={defaultLocale}
      copy={getTranslations(defaultLocale)}
    />
  );
}
