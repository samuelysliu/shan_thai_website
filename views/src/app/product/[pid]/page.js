import React from "react";
import Product_Detail from "@/app/components/product_components/Product_Detail";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";
import config from "@/app/config";
import axios from "axios";

// 生成動態元數據
export async function generateMetadata({ params }) {
  const { pid } = await params;
  const endpoint = config.apiBaseUrl;
  
  try {
    // 獲取商品信息用於元數據
    const response = await axios.get(
      `${endpoint}/frontstage/v1/product_by_pid/${pid}`,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    
    const product = response.data;
    const imageUrl = product.productImageUrl?.[0] || "https://www.shan-thai-team.com/default-image.jpg";
    
    return {
      title: `${product.title_cn} - 善泰團隊 | 南傳聖物`,
      description: `${product.title_cn}。${product.description || "正宗南傳聖物，幫您找到最適合的聖物。"}`,
      keywords: `${product.title_cn},聖物,佛牌,${product.category || "聖物類別"}`,
      robots: "index, follow",
      canonical: `https://www.shan-thai-team.com/product/${pid}`,
      openGraph: {
        title: `${product.title_cn} - 善泰團隊`,
        description: `${product.title_cn}。價格：NT$${product.price}`,
        url: `https://www.shan-thai-team.com/product/${pid}`,
        type: "website",
        images: [
          {
            url: imageUrl,
            width: 800,
            height: 600,
            alt: product.title_cn,
          },
        ],
        siteName: "善泰團隊",
        locale: "zh_TW",
      },
      twitter: {
        card: "summary_large_image",
        title: `${product.title_cn} - 善泰團隊`,
        description: `${product.title_cn}。NT$${product.price}`,
        images: [imageUrl],
      },
    };
  } catch (error) {
    console.error("Failed to fetch product metadata:", error);
    return {
      title: "商品詳情 - 善泰團隊",
      description: "善泰團隊 - 南傳聖物請供",
    };
  }
}

const ProductDetailPage = async ({ params }) => {
  const { pid } = await params;

  return (
    <ClientProvider>
      <Navbar />
      <Container>
        <Product_Detail pid={pid}></Product_Detail>
      </Container>
      <Footer />
    </ClientProvider>
  );
};

export default ProductDetailPage;
