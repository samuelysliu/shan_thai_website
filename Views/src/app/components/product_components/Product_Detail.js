"use client";

import React from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { Container, Row, Col, Card, Button, Spinner } from "react-bootstrap";

const Product_Detail = ({ product }) => {
  const router = useRouter();

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
      <Row xs={2} md={3} xl={4} xxl={5}>
        
      </Row>
    </Container>
  );
}

export default Product_Detail;