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
        timeout: 5000, // 5 秒超時
      }
    );
    
    const product = response.data;
    
    // 驗證必要的產品信息
    if (!product || typeof product !== 'object') {
      throw new Error('Invalid product data');
    }
    
    const imageUrl = product.productImageUrl?.[0] || "https://www.shan-thai-team.com/default-image.jpg";
    const title = product.title_cn || "商品詳情";
    const price = product.price || 0;
    
    return {
      title: `${title} - 善泰團隊 | 南傳聖物`,
      description: `${title}。${product.description || "正宗南傳聖物，幫您找到最適合的聖物。"}`,
      keywords: `${title},聖物,佛牌,${product.category || "聖物類別"}`,
      robots: "index, follow",
      canonical: `https://www.shan-thai-team.com/product/${pid}`,
      openGraph: {
        title: `${title} - 善泰團隊`,
        description: `${title}。價格：NT$${price}`,
        url: `https://www.shan-thai-team.com/product/${pid}`,
        type: "website",
        images: [
          {
            url: imageUrl,
            width: 800,
            height: 600,
            alt: title,
          },
        ],
        siteName: "善泰團隊",
        locale: "zh_TW",
      },
      twitter: {
        card: "summary_large_image",
        title: `${title} - 善泰團隊`,
        description: `${title}。NT$${price}`,
        images: [imageUrl],
      },
    };
  } catch (error) {
    console.error(`Failed to fetch product metadata for PID ${pid}:`, error.message);
    
    // 返回默認元數據而不是拋出錯誤，防止頁面 500
    return {
      title: "商品詳情 - 善泰團隊 | 南傳聖物",
      description: "善泰團隊 - 南傳聖物請供，提供正宗泰國佛牌、四面佛、聖物供應。",
      keywords: "聖物,佛牌,供尊,南傳聖物,泰國佛牌",
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
