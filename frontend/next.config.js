module.exports = {
  reactStrictMode: true,
  swcMinify: true,
  i18n: {
    locales: ['ar', 'en'],
    defaultLocale: 'ar',
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1',
  },
};
