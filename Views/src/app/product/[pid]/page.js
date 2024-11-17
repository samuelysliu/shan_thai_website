"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSelector } from "react-redux";
import { Container, Spinner, Card } from "react-bootstrap";

const ProductDetails = ({ params }) => {
  const { pid } = params; // 從路由參數中取得產品 ID
  const products = useSelector((state) => state.product.products); // 從 Redux Store 獲取產品列表
  const [product, setProduct] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const selectedProduct = products.find((p) => p.pid === parseInt(pid));
    if (selectedProduct) {
      setProduct(selectedProduct); // 設定選中的產品
    } else {
      // 如果沒有找到，跳回產品列表或進行 API 請求
      console.error("產品不存在");
      router.push("/"); // 返回主頁
    }
  }, [pid, products, router]);

  if (!product) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品詳情...</p>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <Card>
        <Card.Img variant="top" src={product.productImageUrl} alt={product.title_cn} />
        <Card.Body>
          <Card.Title>{product.title_cn}</Card.Title>
          <Card.Text>{product.content_cn}</Card.Text>
          <Card.Text>NT. {product.price}</Card.Text>
          <Card.Text>剩餘數量：{product.remain}</Card.Text>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default ProductDetails;
