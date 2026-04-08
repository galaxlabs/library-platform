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
    <main className="app-shell min-h-screen px-4 py-6 text-slate-900 md:px-8 lg:px-10">
      <section className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-7xl flex-col gap-8 rounded-[2rem] border border-black/5 bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.85),rgba(247,242,232,0.7)_48%,rgba(236,228,210,0.92)_100%)] p-5 shadow-[0_28px_120px_rgba(58,50,35,0.12)] md:p-8 lg:p-10">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-3xl">
            <span className="hero-kicker text-[11px] font-semibold text-[var(--accent)]">
              {copy.heroBadge}
            </span>
            <h1 className="mt-5 max-w-4xl text-5xl font-extrabold leading-[1.02] tracking-[-0.05em] text-slate-950 md:text-7xl">
              {copy.heroTitle}
            </h1>
            <p className="mt-6 max-w-2xl text-base leading-8 text-slate-600 md:text-lg">
              {copy.heroDescription}
            </p>
          </div>
          <LanguageSwitcher currentLocale={locale} label={copy.languageLabel} />
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.35fr_0.9fr]">
          <div className="glass-panel rounded-[2rem] p-7 md:p-8">
            <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
              <div className="max-w-xl">
                <p className="hero-kicker text-[11px] font-semibold text-slate-500">
                  Source-Grounded Product
                </p>
                <h2 className="mt-3 text-2xl font-bold tracking-[-0.04em] text-slate-950 md:text-3xl">
                  Premium Arabic-first learning for institutes, scholars, and students
                </h2>
              </div>
              <div className="grid gap-2 text-sm text-slate-500 md:text-right">
                <span>Grounded Q&amp;A</span>
                <span>Scholar Verification</span>
                <span>Structured Book Ingestion</span>
              </div>
            </div>

            <div className="mt-8 grid gap-4 md:grid-cols-3">
              <div className="rounded-[1.6rem] border border-slate-200/80 bg-white/85 p-5">
                <div className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--brand)]">
                  01
                </div>
                <h3 className="mt-4 text-xl font-semibold">{copy.featureGroundedTitle}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-600">
                  {copy.featureGroundedText}
                </p>
              </div>
              <div className="rounded-[1.6rem] border border-slate-200/80 bg-white/85 p-5">
                <div className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--brand)]">
                  02
                </div>
                <h3 className="mt-4 text-xl font-semibold">{copy.featureIngestionTitle}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-600">
                  {copy.featureIngestionText}
                </p>
              </div>
              <div className="rounded-[1.6rem] border border-slate-200/80 bg-white/85 p-5">
                <div className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--brand)]">
                  03
                </div>
                <h3 className="mt-4 text-xl font-semibold">{copy.featureScholarTitle}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-600">
                  {copy.featureScholarText}
                </p>
              </div>
            </div>
          </div>

          <div className="glass-panel rounded-[2rem] p-7 md:p-8">
            <p className="hero-kicker text-[11px] font-semibold text-slate-500">
              Product Access
            </p>
            <div className="mt-4 space-y-4">
              <div className="rounded-[1.5rem] bg-slate-950 px-5 py-6 text-white shadow-2xl shadow-slate-900/20">
                <p className="text-sm uppercase tracking-[0.28em] text-emerald-300">
                  Live Workspace
                </p>
                <p className="mt-4 text-3xl font-bold tracking-[-0.05em]">
                  {copy.brand}
                </p>
                <p className="mt-3 text-sm leading-7 text-slate-300">
                  Switch language, enter the platform, and move between public library,
                  scholar review, and institute dashboards from one coherent shell.
                </p>
              </div>
              <div className="rounded-[1.5rem] border border-slate-200/80 bg-white/80 p-5">
                <p className="text-sm leading-7 text-slate-600">
                  Typography is tuned for a more editorial reading experience and the
                  interface is prepared for both RTL and LTR presentation.
                </p>
              </div>
            </div>

            <div className="mt-8 flex flex-col gap-3">
              <a
                href={loginHref}
                className="inline-flex items-center justify-center rounded-[1.4rem] bg-[var(--brand)] px-6 py-3 text-sm font-semibold text-white transition hover:brightness-110"
              >
                {copy.signIn}
              </a>
              <a
                href={registerHref}
                className="inline-flex items-center justify-center rounded-[1.4rem] border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-50"
              >
                {copy.createAccount}
              </a>
            </div>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-[1.6rem] border border-black/5 bg-white/70 p-5">
            <p className="hero-kicker text-[11px] font-semibold text-slate-500">Library</p>
            <p className="mt-3 text-sm leading-7 text-slate-600">
              Browse public books, editions, references, and structured concepts.
            </p>
          </div>
          <div className="rounded-[1.6rem] border border-black/5 bg-white/70 p-5">
            <p className="hero-kicker text-[11px] font-semibold text-slate-500">Verification</p>
            <p className="mt-3 text-sm leading-7 text-slate-600">
              Surface scholar-reviewed, disputed, and needs-review states clearly.
            </p>
          </div>
          <div className="rounded-[1.6rem] border border-black/5 bg-white/70 p-5">
            <p className="hero-kicker text-[11px] font-semibold text-slate-500">Learning</p>
            <p className="mt-3 text-sm leading-7 text-slate-600">
              Turn grounded references into guided study, practice, and revision workflows.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
