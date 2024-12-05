"use client";

import React from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { Container, Row, Col, Card, Button, Spinner } from "react-bootstrap";

const Product_Grid = ({ initialProducts }) => {
  const router = useRouter();

  if (!initialProducts) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品...</p>
      </Container>
    );
  } else if (initialProducts.length === 0) {
    return (
      <Container className="text-center my-4">
        <p className="mt-2">目前無產品上架</p>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <Row xs={2} md={3} xl={4} xxl={5}>
        {initialProducts.map((product) => (
          <Col xs={6} md={3} key={product.pid} className="mb-4">
            <Card className="text-center product-card">
              <Card.Img
                variant="top"
                src={product.productImageUrl}
                alt={product.title_cn}
                onClick={() => router.push(`/product/${product.pid}`)}
                style={{ cursor: "pointer" }} />
              <Card.Body>
                <Card.Title>{product.title_cn}</Card.Title>
                <Card.Text>NT. {product.price}</Card.Text>
                <Button variant="outline-dark" size="sm">購買</Button>
                <Button variant="outline-dark" size="sm" onClick={() => dispatch(addToCart(product))}>加入購物車</Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default Product_Grid;