import React from "react";
import Product_Detail from "@/app/components/product_components/Product_Detail";

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
  const { pid } = params; // 從路由參數中取得產品 ID
  const product = await fetchProductDetail(pid); // 伺服器端獲取產品數據


  return (
    <>
      <Product_Detail product={product}></Product_Detail>
    </>
  );
};

export default ProductDetailPage;
