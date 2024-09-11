/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
        {
            source: '/:path*',      // Routes starting with /api/
            destination: 'http://localhost:5000/:path*',  // Proxy to your backend API
        },
        ];
    },
};

export default nextConfig;
