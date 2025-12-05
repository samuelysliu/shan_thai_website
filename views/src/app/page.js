import React from "react";
import HomePageClient from "./components/Homepage";
import ClientProvider from "./components/Client_Provider";

export const metadata = {
  title: "善泰團隊 - 南傳聖物請供 | 佛牌、四面佛、供尊",
  description: "想要求財、改運、佛牌、供尊，通通可以在這裡找到。善泰團隊，幫您找到最適合的聖物。提供正宗泰國佛牌、四面佛、聖物供應。",
  keywords: "佛牌,四面佛,求財,改運,聖物,供尊,南傳聖物,泰國佛牌",
  robots: "index, follow",
  canonical: "https://www.shan-thai-team.com",
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
  },
};

const HomePage = async () => {
  return (
    <ClientProvider>
      <HomePageClient />
    </ClientProvider>
  );
};

export default HomePage;
