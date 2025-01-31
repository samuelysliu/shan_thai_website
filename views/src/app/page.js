// pages/index.js
import React from "react";
import HomePageClient from "./components/Homepage";
import ClientProvider from "./components/Client_Provider";
import Head from "next/head";

const HomePage = async () => {

  return (
    <>
      {/* SEO 信息放在這裡 */}
      <Head>
        <title>善泰團隊 - 南傳聖物請供</title>
        <meta name="description" content="想要求財、改運、佛牌、供尊，通通可以在這裡找到。善泰團隊，幫您找到最適合的聖物。" />
        <meta name="keywords" content="求財、改運、法事、佛牌、四面佛、佛教聖物、南傳聖物" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://www.shan-thai-team.com" />
      </Head>
      <ClientProvider>
        <HomePageClient />
      </ClientProvider>
    </>

  );
};

export default HomePage;
