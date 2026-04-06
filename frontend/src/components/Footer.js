import Link from 'next/link';

export default function Footer() {
    return (
        <footer className="footer">
            <div className="container">
                <p>
                    Built with ❤️ by developers, for developers · <Link href="/">DevPulse</Link> © {new Date().getFullYear()}
                </p>
            </div>
        </footer>
    );
}
