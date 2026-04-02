/** @type {import('next').NextConfig} */
const isTauriBuild = process.env.TAURI_BUILD === '1';

const nextConfig = {
  // Static export for Tauri production builds (no Next.js server needed)
  ...(isTauriBuild ? { output: 'export', trailingSlash: true } : {}),

  images: {
    // Static export requires unoptimized images (no Next.js image server)
    unoptimized: isTauriBuild,
    domains: ['localhost'],
  },

  async rewrites() {
    // Rewrites are only active in the Next.js dev/server mode, not static export
    if (isTauriBuild) return [];

    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Only add rewrites if backend URL is defined and valid
    if (!backendUrl || backendUrl === 'undefined') {
      return [];
    }

    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
