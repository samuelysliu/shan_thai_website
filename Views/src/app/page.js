// pages/index.js
import React from "react";
import HomePageClient from "./components/Homepage";
import ClientProvider from "./components/Client_Provider";
import config from './config';


// 提前讀取產品清單，以利SEO
const fetchProducts = async () => {
  let endpoint = config.apiBaseUrl;
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
async function fetchProductTags() {
  let endpoint = config.apiBaseUrl;
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
  const products = await fetchProducts(); // 伺服器端獲取產品數據
  const productTags = await fetchProductTags(); // 伺服器端獲取產品標籤數據

  return (
    <ClientProvider>
      <HomePageClient products={products} productTags={productTags} />
    </ClientProvider>
  );
};

export default HomePage;
