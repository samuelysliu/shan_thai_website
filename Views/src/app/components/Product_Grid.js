"use client";  // 設定為客戶端組件

import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const products = [
  { id: 1, name: "Product 1", price: "NT.1,299", img: "/path/to/image1.jpg" },
  { id: 2, name: "Product 2", price: "NT.1,299", img: "/path/to/image2.jpg" },
  { id: 3, name: "Product 3", price: "NT.1,299", img: "/path/to/image3.jpg" },
  { id: 4, name: "Product 4", price: "NT.1,299", img: "/path/to/image4.jpg" },
  { id: 5, name: "Product 5", price: "NT.1,299", img: "/path/to/image4.jpg" },
  { id: 6, name: "Product 6", price: "NT.1,299", img: "/path/to/image4.jpg" },
  { id: 7, name: "Product 7", price: "NT.1,299", img: "/path/to/image4.jpg" },
  // 更多產品...
];

export default function Product_Grid() {
  return (
    <Container className="my-4">
      <Row xs={2} md={3} xl={4} xxl={5}>
        {products.map(product => (
          <Col xs={6} md={3} key={product.id} className="mb-4">
            <Card className="text-center product-card">
              <Card.Img variant="top" src={product.img} alt="產品圖片" />
              <Card.Body>
                <Card.Title>{product.name}</Card.Title>
                <Card.Text>{product.price}</Card.Text>
                <Button variant="outline-dark" size="sm">購買</Button>
                <Button variant="outline-dark" size="sm">加入購物車</Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}
