import type { Metadata } from 'next';
import '../styles/globals.css';
import { AuthProvider } from '../contexts/AuthContext';

export const metadata: Metadata = {
  title: 'Maktaba Ilmiah',
  description: 'Maktaba Ilmiah multilingual scholarly AI platform for Arabic and Islamic books',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
