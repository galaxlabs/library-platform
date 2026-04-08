import LanguageSwitcher from './LanguageSwitcher';
import { TranslationBundle, defaultLocale } from '../lib/i18n';

type HomePageContentProps = {
  locale?: string;
  copy: TranslationBundle;
};

export default function HomePageContent({
  locale = defaultLocale,
  copy,
}: HomePageContentProps) {
  const loginHref = locale === defaultLocale ? '/login' : `/${locale}/login`;
  const registerHref =
    locale === defaultLocale ? '/register' : `/${locale}/register`;

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto flex min-h-screen max-w-7xl flex-col justify-center px-6 py-16">
        <div className="flex flex-col gap-6">
          <LanguageSwitcher currentLocale={locale} label={copy.languageLabel} />
          <div className="max-w-3xl">
            <span className="inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-1 text-sm text-emerald-200">
              {copy.heroBadge}
            </span>
            <h1 className="mt-6 text-4xl font-bold leading-tight text-white md:text-6xl">
              {copy.heroTitle}
            </h1>
            <p className="mt-6 text-lg leading-8 text-slate-300">
              {copy.heroDescription}
            </p>
          </div>
        </div>

        <div className="mt-10 grid gap-4 md:grid-cols-3">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-slate-900/30">
            <h2 className="text-xl font-semibold">{copy.featureGroundedTitle}</h2>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              {copy.featureGroundedText}
            </p>
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-slate-900/30">
            <h2 className="text-xl font-semibold">{copy.featureIngestionTitle}</h2>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              {copy.featureIngestionText}
            </p>
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-slate-900/30">
            <h2 className="text-xl font-semibold">{copy.featureScholarTitle}</h2>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              {copy.featureScholarText}
            </p>
          </div>
        </div>

        <div className="mt-10 flex flex-col gap-4 sm:flex-row">
          <a
            href={loginHref}
            className="inline-flex items-center justify-center rounded-2xl bg-emerald-400 px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-300"
          >
            {copy.signIn}
          </a>
          <a
            href={registerHref}
            className="inline-flex items-center justify-center rounded-2xl border border-white/15 px-6 py-3 text-sm font-semibold text-white transition hover:bg-white/5"
          >
            {copy.createAccount}
          </a>
        </div>
      </section>
    </main>
  );
}
