import localFont from "next/font/local";
import "./globals.css";
import "./backstage.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import config from "./config";


const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

const gaId = config.gaId;

export const metadata = {
  title: "善泰團隊 - 南傳聖物請供 | 佛牌、四面佛、供尊",
  description: "想要求財、改運、佛牌、供尊，通通可以在這裡找到。善泰團隊，幫您找到最適合的聖物。提供正宗泰國佛牌、四面佛、聖物供應。",
  keywords: "佛牌,四面佛,求財,改運,聖物,供尊,南傳聖物,泰國佛牌",
  robots: "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
  canonical: "https://www.shan-thai-team.com",
  alternates: {
    canonical: "https://www.shan-thai-team.com",
  },
  openGraph: {
    title: "善泰團隊 - 南傳聖物請供",
    description: "想要求財、改運、佛牌、供尊，通通可以在這裡找到。善泰團隊，幫您找到最適合的聖物。",
    url: "https://www.shan-thai-team.com",
    siteName: "善泰團隊",
    locale: "zh_TW",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "善泰團隊 - 南傳聖物請供",
    description: "想要求財、改運、佛牌、供尊，通通可以在這裡找到。",
    creator: "@shanthaiteam",
  },
  authors: [{ name: "善泰團隊" }],
  creator: "善泰團隊",
  publisher: "善泰團隊",
  applicationName: "善泰團隊商城",
};

export const viewport = "width=device-width, initial-scale=1.0, maximum-scale=5.0";

export default function RootLayout({ children }) {
  return (
    <html lang="zh-TW">
      <head>
        {/* Google Analytics */}
        <script async src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`} />
        <script>
          {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', '${gaId}');
          `}
        </script>
        
        {/* 組織結構化數據 */}
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "善泰團隊",
            "url": "https://www.shan-thai-team.com",
            "description": "南傳聖物請供，提供佛牌、四面佛等聖物",
            "logo": "https://www.shan-thai-team.com/logo.png",
            "sameAs": [
              "https://www.facebook.com/shanthaiteam"
            ],
            "address": {
              "@type": "PostalAddress",
              "addressCountry": "TW"
            }
          })}
        </script>

        {/* 本地商城結構化數據 */}
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "善泰團隊",
            "url": "https://www.shan-thai-team.com",
            "description": "南傳聖物請供",
            "priceRange": "NTD"
          })}
        </script>
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable}`} >
        {children}
      </body>
    </html>
  );
}
