"use client";

import React from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { Container, Row, Col, Image, Button, Card } from "react-bootstrap";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示

const Product_Detail = ({ product }) => {
  const router = useRouter();

  const handleBuyNow = () => {
    // 立即購買的邏輯
    console.log("立即購買", product.pid);
  };

  if (!product) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品...</p>
      </Container>
    );
  } else if (product.length === 0) {
    return (
      <Container className="text-center my-4">
        <p className="mt-2">查無此產品</p>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <Button variant="link" onClick={() => router.back()} className="mb-3">
        <FaArrowLeft />返回
      </Button>
      <Row className="align-items-start">
        <Col xs={12} md={6} className="text-center">
          <Image src={product.productImageUrl} alt={product.title_cn} fluid rounded />
        </Col>
        <Col xs={12} md={6}>
          <Card className="border-0">
            <Card.Body>
              <Card.Title className="product-title" as="h1">{product.title_cn}</Card.Title>
              <Card.Text className="product-price text-muted">
                <h3>NT. {product.price}</h3>
              </Card.Text>
              <Card.Text className="product-stock">
                <span>庫存數量：{product.remain}</span>
              </Card.Text>
              {/* 按鈕區域 */}
              <div className="d-grid gap-2 mt-4">
                <Button
                  variant="outline-primary"
                  size="lg"
                  onClick={handleAddToCart}
                  disabled={product.remain <= 0}
                >
                  加入購物車
                </Button>
                <Button
                  variant="primary"
                  size="lg"
                  onClick={() => dispatch(addToCart(product))}
                  disabled={product.remain <= 0}
                >
                  直接購買
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      {/* 底部：產品詳細說明 */}
      <Row className="mt-5">
        <Col>
          <h3>產品說明</h3>
          <p>{product.content_cn}</p>
        </Col>
      </Row>
    </Container>
  );
}

export default Product_Detail;