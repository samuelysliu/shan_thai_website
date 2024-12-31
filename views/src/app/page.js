// pages/index.js
import React from "react";
import HomePageClient from "./components/Homepage";
import ClientProvider from "./components/Client_Provider";
import config from "./config";
import Head from "next/head";

// 提前讀取產品清單，以利SEO
const fetchProducts = async (endpoint) => {
  try {
    const response = await fetch(`${endpoint}/frontstage/v1/product`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    return await response.json();
  } catch (err) {
    console.error("無法加載產品清單", err);
    return [];
  }
}

// 伺服器端獲取產品標籤列表
async function fetchProductTags(endpoint) {
  let productTags = [];
  try {
    const response = await fetch(endpoint + "/frontstage/v1/product_tag", { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Failed to fetch product tags');
    }
    productTags = await response.json();
  } catch (err) {
    console.error("無法加載產品標籤清單", err);
  }
  return productTags;
}


const HomePage = async () => {
  const endpoint = config.apiBaseUrl;
  const products = await fetchProducts(endpoint); // 伺服器端獲取產品數據
  const productTags = await fetchProductTags(endpoint); // 伺服器端獲取產品標籤數據

  return (
    <>
      {/* SEO 信息放在這裡 */}
      <Head>
        <title>善泰團隊 - 南傳聖物請供</title>
        <meta name="description" content="想要求財、改運、佛牌、供尊，通通可以在這裡找到。善泰團隊，幫您找到最適合的聖物。" />
        <meta name="keywords" content="求財、改運、法事、佛牌、四面佛、佛教聖物、南傳聖物" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://your-domain.com" />
      </Head>
      <ClientProvider>
        <HomePageClient products={products} productTags={productTags} />
      </ClientProvider>
    </>

  );
};

export default HomePage;
