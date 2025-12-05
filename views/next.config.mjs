/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    
    // 圖片優化配置
    images: {
        domains: ['www.shan-thai-team.com', 'localhost'],
        formats: ['image/webp', 'image/avif'],
        deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
        imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
        minimumCacheTTL: 31536000, // 1年快取
    },

    // 將環境變數暴露給應用程序
    env: {
        NEXT_PUBLIC_ENV: process.env.NEXT_PUBLIC_ENV || "production",
    },
    
    // 性能和SEO配置
    compress: true,
    poweredByHeader: false,
    
    // 重定向配置（可選，根據需要添加）
    async redirects() {
        return [
            // 舊URL重定向示例
            // {
            //     source: '/old-product/:id',
            //     destination: '/product/:id',
            //     permanent: true,
            // },
        ];
    },

    // 自定義Headers - 添加SEO和安全相關Header
    async headers() {
        return [
            {
                source: '/:path*',
                headers: [
                    {
                        key: 'X-Content-Type-Options',
                        value: 'nosniff'
                    },
                    {
                        key: 'X-Frame-Options',
                        value: 'SAMEORIGIN'
                    },
                    {
                        key: 'X-XSS-Protection',
                        value: '1; mode=block'
                    },
                    {
                        key: 'Referrer-Policy',
                        value: 'strict-origin-when-cross-origin'
                    },
                ],
            },
        ];
    },
};

export default nextConfig;

