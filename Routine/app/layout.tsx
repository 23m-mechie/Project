import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Diet Plan Timeline',
  description: 'Daily structured high-protein diet plan timeline.'
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}

