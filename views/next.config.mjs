/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,

    // 將環境變數暴露給應用程序
    env: {
        NEXT_PUBLIC_ENV: process.env.NEXT_PUBLIC_ENV || "production", // 默認值為 "local"
    },
};

export default nextConfig;
