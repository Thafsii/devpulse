import '../styles/globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export const metadata = {
  title: 'DevPulse — Developer Updates Dashboard',
  description: 'Stay updated with the latest software technologies, tools, frameworks, and releases. Aggregated insights for developers.',
  keywords: ['developer tools', 'frameworks', 'updates', 'trending', 'tech news'],
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
