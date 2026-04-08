'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import axios from 'axios';

import LanguageSwitcher from './LanguageSwitcher';
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

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/login/`,
        { email, password }
      );

      const { tokens, user } = response.data;
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
      localStorage.setItem('user', JSON.stringify(user));
      router.push('/dashboard');
    } catch (err: any) {
      setError(getApiErrorMessage(err, copy.loginError));
    } finally {
      setLoading(false);
    }
  };

  const registerHref =
    locale === defaultLocale ? '/register' : `/${locale}/register`;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="mx-auto flex min-h-screen w-full max-w-md items-center">
        <div className="w-full">
          <div className="mb-6 flex justify-center">
            <LanguageSwitcher currentLocale={locale} label={copy.languageLabel} />
          </div>
          <div className="mb-8 text-center">
            <h1 className="mb-2 text-3xl font-bold text-gray-900">{copy.brand}</h1>
            <p className="text-gray-600">{copy.tagline}</p>
          </div>

          <div className="space-y-6 rounded-xl bg-white p-8 shadow-lg">
            {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 p-4">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  {copy.emailLabel}
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                  placeholder="you@example.com"
                  className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  {copy.passwordLabel}
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  placeholder="••••••••"
                  className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? copy.loadingLogin : copy.signIn}
              </button>
            </form>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="bg-white px-2 text-gray-500">{copy.or}</span>
              </div>
            </div>

            <div className="text-center">
              <p className="mb-3 text-sm text-gray-600">{copy.noAccount}</p>
              <Link
                href={registerHref}
                className="inline-block rounded-lg bg-gray-100 px-6 py-2 font-medium text-gray-900 transition hover:bg-gray-200"
              >
                {copy.createAccount}
              </Link>
            </div>
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

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/register/`,
        {
          email,
          full_name: fullName,
          arabic_name: arabicName,
          phone,
          preferred_lang_pair: preferredLangPair,
          password,
          password_confirm: passwordConfirm,
        }
      );

      const { tokens, user } = response.data;
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
      localStorage.setItem('user', JSON.stringify(user));
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="mx-auto flex min-h-screen w-full max-w-xl items-center">
        <div className="w-full">
          <div className="mb-6 flex justify-center">
            <LanguageSwitcher currentLocale={locale} label={copy.languageLabel} />
          </div>
          <div className="mb-8 text-center">
            <h1 className="mb-2 text-3xl font-bold text-gray-900">{copy.brand}</h1>
            <p className="text-gray-600">{copy.registerTitle}</p>
          </div>

          <div className="space-y-6 rounded-xl bg-white p-8 shadow-lg">
            {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 p-4">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    {labels.fullName}
                  </label>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(event) => setFullName(event.target.value)}
                    required
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    {labels.arabicName}
                  </label>
                  <input
                    type="text"
                    value={arabicName}
                    onChange={(event) => setArabicName(event.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    {copy.emailLabel}
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                    placeholder="you@example.com"
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    {labels.phone}
                  </label>
                  <input
                    type="text"
                    value={phone}
                    onChange={(event) => setPhone(event.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  {labels.preferredLanguage}
                </label>
                <select
                  value={preferredLangPair}
                  onChange={(event) => setPreferredLangPair(event.target.value)}
                  className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                >
                  <option value="ar-en">{labels.arabicEnglish}</option>
                  <option value="ar-ur">{labels.arabicUrdu}</option>
                </select>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    {copy.passwordLabel}
                  </label>
                  <input
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                    placeholder="••••••••"
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    {labels.passwordConfirm}
                  </label>
                  <input
                    type="password"
                    value={passwordConfirm}
                    onChange={(event) => setPasswordConfirm(event.target.value)}
                    required
                    placeholder="••••••••"
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-transparent focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? labels.signingUp : copy.createAccount}
              </button>
            </form>

            <div className="text-center">
              <p className="mb-3 text-sm text-gray-600">{labels.haveAccount}</p>
              <Link
                href={loginHref}
                className="inline-block rounded-lg bg-gray-100 px-6 py-2 font-medium text-gray-900 transition hover:bg-gray-200"
              >
                {copy.signIn}
              </Link>
            </div>
          </div>

          <p className="mt-6 text-center text-xs text-gray-600">{copy.footer}</p>
        </div>
      </div>
    </div>
  );
}
