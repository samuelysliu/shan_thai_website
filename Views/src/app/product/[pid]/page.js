import React from "react";
import Product_Detail from "@/app/components/product_components/Product_Detail";
import config from "@/app/config";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";
import Head from "next/head";

// 提前讀取產品清單，以利SEO
const fetchProductDetail = async (pid) => {
  let endpoint = config.apiBaseUrl;
  try {
    const response = await fetch(`${endpoint}/frontstage/v1/product_by_pid/${pid}`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    return await response.json();
  } catch (err) {
    console.error("無法加載產品清單", err);
    return [];
  }
}

const ProductDetailPage = async ({ params }) => {
  const { pid } = await params; // 從路由參數中取得產品 ID
  const product = await fetchProductDetail(pid); // 伺服器端獲取產品數據


  return (
    <>
      <Head>
        <title>{product.title_cn}</title>
        <meta name="description" content={product.content_cn} />
        <meta name="keywords" content="求財、改運、法事、佛牌、四面佛、佛教聖物、南傳聖物" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://your-domain.com" />
      </Head>
      <ClientProvider>
        <Navbar />
        <Container>
          <Product_Detail product={product}></Product_Detail>
        </Container>
        <Footer />
      </ClientProvider>
    </>
  );
};

export default ProductDetailPage;
