/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
        {
            source: '/:path*',      // Routes starting with /api/
            destination: 'http://localhost:3000/:path*',  // Proxy to your backend API
        },
        ];
    },
};

export default nextConfig;
