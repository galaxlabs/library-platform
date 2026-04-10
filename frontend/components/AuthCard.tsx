'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';

import LanguageSwitcher from './LanguageSwitcher';
import { useAuth } from '../contexts/AuthContext';
import { TranslationBundle, defaultLocale } from '../lib/i18n';

type AuthCardProps = {
  locale?: string;
  copy: TranslationBundle;
};

function getApiErrorMessage(error: any, fallback: string): string {
  const data = error?.response?.data;

  if (typeof data?.detail === 'string') {
    return data.detail;
  }

  if (typeof data?.password === 'string') {
    return data.password;
  }

  if (Array.isArray(data?.password) && data.password[0]) {
    return data.password[0];
  }

  if (Array.isArray(data?.non_field_errors) && data.non_field_errors[0]) {
    return data.non_field_errors[0];
  }

  if (data && typeof data === 'object') {
    for (const value of Object.values(data)) {
      if (typeof value === 'string') {
        return value;
      }
      if (Array.isArray(value) && value[0]) {
        return String(value[0]);
      }
    }
  }

  return fallback;
}

export function LoginCard({
  locale = defaultLocale,
  copy,
}: AuthCardProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  const { login } = useAuth();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(getApiErrorMessage(err, copy.loginError));
    } finally {
      setLoading(false);
    }
  };

  const registerHref =
    locale === defaultLocale ? '/register' : `/${locale}/register`;

  const roleLineByLocale: Record<string, string> = {
    en: 'For students, learners, scholars, and institutions',
    ar: 'للطلبة والمتعلمين والعلماء والمؤسسات',
    ur: 'طلبہ، سیکھنے والوں، علما اور اداروں کے لیے',
  };

  const roleLine = roleLineByLocale[locale] ?? roleLineByLocale.en;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,rgba(183,121,51,0.14),transparent_24%),radial-gradient(circle_at_top_right,rgba(29,107,87,0.12),transparent_22%),linear-gradient(180deg,#f7f2e8_0%,#f3ecdf_50%,#efe7d8_100%)] px-4 py-8">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl items-center">
        <div className="w-full">
          <div className="mb-6 flex justify-center">
            <LanguageSwitcher currentLocale={locale} label={copy.languageLabel} />
          </div>
          <div className="grid gap-6 xl:grid-cols-[1.08fr_0.92fr]">
            <section className="rounded-[2rem] bg-[linear-gradient(145deg,#172033_0%,#1f5f57_55%,#d48d3f_140%)] p-8 text-white shadow-[0_30px_80px_rgba(40,32,18,0.18)] md:p-10">
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-emerald-200">
                {copy.brand}
              </p>
              <h1 className="mt-4 max-w-xl text-4xl font-extrabold tracking-[-0.06em] md:text-6xl">
                {copy.signIn}
              </h1>
              <p className="mt-5 max-w-2xl text-base leading-8 text-slate-200 md:text-lg">
                {copy.tagline}
              </p>
              <p className="mt-4 text-sm font-medium text-amber-100/90">
                {roleLine}
              </p>

              <div className="mt-10 grid gap-4 md:grid-cols-3">
                <div className="rounded-[1.4rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
                  <p className="text-sm font-semibold text-white">Students</p>
                  <p className="mt-2 text-sm leading-6 text-slate-200">
                    Read lessons, save answers, and follow revision work.
                  </p>
                </div>
                <div className="rounded-[1.4rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
                  <p className="text-sm font-semibold text-white">Scholars</p>
                  <p className="mt-2 text-sm leading-6 text-slate-200">
                    Review knowledge, check references, and guide learning.
                  </p>
                </div>
                <div className="rounded-[1.4rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
                  <p className="text-sm font-semibold text-white">Institutions</p>
                  <p className="mt-2 text-sm leading-6 text-slate-200">
                    Manage classes, books, and trusted study workflows.
                  </p>
                </div>
              </div>
            </section>

            <section className="rounded-[2rem] border border-white/60 bg-white/85 p-8 shadow-[0_28px_70px_rgba(40,32,18,0.12)] backdrop-blur md:p-10">
              <div className="mb-8">
                <h2 className="text-3xl font-bold tracking-[-0.05em] text-slate-950">
                  {copy.signIn}
                </h2>
                <p className="mt-3 text-base leading-7 text-slate-600">
                  Use your email and password to open your learning space.
                </p>
              </div>

              {error && (
                <div className="mb-6 rounded-[1.2rem] border border-red-200 bg-red-50 px-4 py-4">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {copy.emailLabel}
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                    placeholder="you@example.com"
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {copy.passwordLabel}
                  </label>
                  <input
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                    placeholder="••••••••"
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="h-14 w-full rounded-[1.15rem] bg-slate-950 px-5 text-base font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? copy.loadingLogin : copy.signIn}
                </button>
              </form>

              <div className="my-8 flex items-center gap-4">
                <div className="h-px flex-1 bg-slate-200"></div>
                <span className="text-sm font-medium text-slate-500">{copy.or}</span>
                <div className="h-px flex-1 bg-slate-200"></div>
              </div>

              <div className="text-center">
                <p className="mb-4 text-sm text-slate-600">{copy.noAccount}</p>
                <Link
                  href={registerHref}
                  className="inline-flex min-h-[3.25rem] items-center justify-center rounded-[1.15rem] bg-[rgba(247,244,238,0.95)] px-6 text-base font-semibold text-slate-900 ring-1 ring-slate-200 transition hover:bg-white"
                >
                  {copy.createAccount}
                </Link>
              </div>
            </section>
          </div>

          <p className="mt-6 text-center text-xs text-gray-600">{copy.footer}</p>
        </div>
      </div>
    </div>
  );
}

export function RegisterCard({
  locale = defaultLocale,
  copy,
}: AuthCardProps) {
  const [fullName, setFullName] = useState('');
  const [arabicName, setArabicName] = useState('');
  const [phone, setPhone] = useState('');
  const [preferredLangPair, setPreferredLangPair] = useState('ar-en');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  const { register } = useAuth();

  const loginHref =
    locale === defaultLocale ? '/login' : `/${locale}/login`;

  const registerErrorByLocale: Record<string, string> = {
    en: 'Registration failed. Please review your information.',
    ar: 'فشل إنشاء الحساب. يرجى مراجعة البيانات المدخلة.',
    ur: 'اکاؤنٹ بنانا ناکام ہوا۔ براہ کرم درج کی گئی معلومات چیک کریں۔',
  };

  const labelsByLocale: Record<string, Record<string, string>> = {
    en: {
      fullName: 'Full Name',
      arabicName: 'Arabic Name',
      phone: 'Phone',
      preferredLanguage: 'Preferred Language Pair',
      passwordConfirm: 'Confirm Password',
      signingUp: 'Creating account...',
      haveAccount: 'Already have an account?',
      arabicEnglish: 'Arabic + English',
      arabicUrdu: 'Arabic + Urdu',
    },
    ar: {
      fullName: 'الاسم الكامل',
      arabicName: 'الاسم بالعربية',
      phone: 'رقم الهاتف',
      preferredLanguage: 'اللغة المفضلة',
      passwordConfirm: 'تأكيد كلمة المرور',
      signingUp: 'جاري إنشاء الحساب...',
      haveAccount: 'لديك حساب بالفعل؟',
      arabicEnglish: 'العربية + الإنجليزية',
      arabicUrdu: 'العربية + الأوردية',
    },
    ur: {
      fullName: 'پورا نام',
      arabicName: 'عربی نام',
      phone: 'فون نمبر',
      preferredLanguage: 'پسندیدہ زبان',
      passwordConfirm: 'پاس ورڈ کی تصدیق',
      signingUp: 'اکاؤنٹ بنایا جا رہا ہے...',
      haveAccount: 'کیا آپ کے پاس پہلے سے اکاؤنٹ ہے؟',
      arabicEnglish: 'عربی + انگریزی',
      arabicUrdu: 'عربی + اردو',
    },
  };

  const labels = labelsByLocale[locale] ?? labelsByLocale.en;
  const roleLineByLocale: Record<string, string> = {
    en: 'For students, learners, scholars, and institutions',
    ar: 'للطلبة والمتعلمين والعلماء والمؤسسات',
    ur: 'طلبہ، سیکھنے والوں، علما اور اداروں کے لیے',
  };
  const roleLine = roleLineByLocale[locale] ?? roleLineByLocale.en;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register({
        email,
        full_name: fullName,
        arabic_name: arabicName,
        phone,
        preferred_lang_pair: preferredLangPair,
        password,
        password_confirm: passwordConfirm,
      });
      router.push('/dashboard');
    } catch (err: any) {
      setError(
        getApiErrorMessage(
          err,
          registerErrorByLocale[locale] ?? registerErrorByLocale.en
        )
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,rgba(183,121,51,0.14),transparent_24%),radial-gradient(circle_at_top_right,rgba(29,107,87,0.12),transparent_22%),linear-gradient(180deg,#f7f2e8_0%,#f3ecdf_50%,#efe7d8_100%)] px-4 py-8">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl items-center">
        <div className="w-full">
          <div className="mb-6 flex justify-center">
            <LanguageSwitcher currentLocale={locale} label={copy.languageLabel} />
          </div>
          <div className="grid gap-6 xl:grid-cols-[1.04fr_0.96fr]">
            <section className="rounded-[2rem] bg-[linear-gradient(145deg,#172033_0%,#1f5f57_55%,#d48d3f_140%)] p-8 text-white shadow-[0_30px_80px_rgba(40,32,18,0.18)] md:p-10">
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-emerald-200">
                {copy.brand}
              </p>
              <h1 className="mt-4 max-w-2xl text-4xl font-extrabold tracking-[-0.06em] md:text-6xl">
                {copy.registerTitle}
              </h1>
              <p className="mt-5 max-w-2xl text-base leading-8 text-slate-200 md:text-lg">
                Create your account and start using the study space, saved answers, and chat tools.
              </p>
              <p className="mt-4 text-sm font-medium text-amber-100/90">
                {roleLine}
              </p>

              <div className="mt-10 grid gap-4 md:grid-cols-3">
                <div className="rounded-[1.4rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
                  <p className="text-sm font-semibold text-white">Learners</p>
                  <p className="mt-2 text-sm leading-6 text-slate-200">
                    Keep your reading, practice, and saved answers together.
                  </p>
                </div>
                <div className="rounded-[1.4rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
                  <p className="text-sm font-semibold text-white">Scholars</p>
                  <p className="mt-2 text-sm leading-6 text-slate-200">
                    Use one account to read, review, and respond with context.
                  </p>
                </div>
                <div className="rounded-[1.4rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
                  <p className="text-sm font-semibold text-white">Institutions</p>
                  <p className="mt-2 text-sm leading-6 text-slate-200">
                    Organize users, learning paths, and trusted study content.
                  </p>
                </div>
              </div>
            </section>

            <section className="rounded-[2rem] border border-white/60 bg-white/88 p-8 shadow-[0_28px_70px_rgba(40,32,18,0.12)] backdrop-blur md:p-10">
              <div className="mb-8">
                <h2 className="text-3xl font-bold tracking-[-0.05em] text-slate-950">
                  {copy.createAccount}
                </h2>
                <p className="mt-3 text-base leading-7 text-slate-600">
                  Enter your details below to create a new account.
                </p>
              </div>

              {error && (
                <div className="mb-6 rounded-[1.2rem] border border-red-200 bg-red-50 px-4 py-4">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {labels.fullName}
                  </label>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(event) => setFullName(event.target.value)}
                    required
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {labels.arabicName}
                  </label>
                  <input
                    type="text"
                    value={arabicName}
                    onChange={(event) => setArabicName(event.target.value)}
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {copy.emailLabel}
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                    placeholder="you@example.com"
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {labels.phone}
                  </label>
                  <input
                    type="text"
                    value={phone}
                    onChange={(event) => setPhone(event.target.value)}
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>
              </div>

              <div>
                <label className="mb-3 block text-sm font-semibold text-slate-700">
                  {labels.preferredLanguage}
                </label>
                <select
                  value={preferredLangPair}
                  onChange={(event) => setPreferredLangPair(event.target.value)}
                  className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                >
                  <option value="ar-en">{labels.arabicEnglish}</option>
                  <option value="ar-ur">{labels.arabicUrdu}</option>
                </select>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {copy.passwordLabel}
                  </label>
                  <input
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                    placeholder="••••••••"
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold text-slate-700">
                    {labels.passwordConfirm}
                  </label>
                  <input
                    type="password"
                    value={passwordConfirm}
                    onChange={(event) => setPasswordConfirm(event.target.value)}
                    required
                    placeholder="••••••••"
                    className="h-14 w-full rounded-[1.15rem] border border-slate-200 bg-[rgba(250,248,242,0.9)] px-5 text-base text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="h-14 w-full rounded-[1.15rem] bg-slate-950 px-5 text-base font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? labels.signingUp : copy.createAccount}
              </button>
            </form>

              <div className="my-8 flex items-center gap-4">
                <div className="h-px flex-1 bg-slate-200"></div>
                <span className="text-sm font-medium text-slate-500">{copy.or}</span>
                <div className="h-px flex-1 bg-slate-200"></div>
              </div>

              <div className="text-center">
                <p className="mb-4 text-sm text-slate-600">{labels.haveAccount}</p>
                <Link
                  href={loginHref}
                  className="inline-flex min-h-[3.25rem] items-center justify-center rounded-[1.15rem] bg-[rgba(247,244,238,0.95)] px-6 text-base font-semibold text-slate-900 ring-1 ring-slate-200 transition hover:bg-white"
                >
                  {copy.signIn}
                </Link>
              </div>
            </section>
          </div>

          <p className="mt-6 text-center text-xs text-gray-600">{copy.footer}</p>
        </div>
      </div>
    </div>
  );
}
