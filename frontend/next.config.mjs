/** @type {import('next').NextConfig} */
const nextConfig = {
    // No 'output: export' — DevPulse uses SSR features (API routes, getSession)
    // which require a Node.js runtime. Static export would break auth and the
    // Netlify plugin handles deployment automatically.
    reactStrictMode: true,

    // Allow images from Supabase storage (avatars, logos)
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: '**.supabase.co',
            },
        ],
    },
};

export default nextConfig;
