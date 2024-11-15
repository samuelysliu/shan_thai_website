"use client";  // 設定為客戶端組件

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

export default function Product_Menu() {
  const router = useRouter();

  const handleNavLink = (path) => {
    router.push(path);
  };

  return (
    <Container fluid className="product-menu-container">
      <Row className="product_menu">
        <Col xs="auto"><a onClick={() => handleNavLink('/')}>Category 1</a></Col>
        <Col xs="auto"><a onClick={() => handleNavLink('/')}>Category 2</a></Col>
        <Col xs="auto"><a onClick={() => handleNavLink('/')}>Category 3</a></Col>
        <Col xs="auto"><a onClick={() => handleNavLink('/')}>Category 4</a></Col>
        <Col xs="auto"><a onClick={() => handleNavLink('/')}>Category 5</a></Col>
        <Col xs="auto"><a onClick={() => handleNavLink('/')}>Category 6</a></Col>
        <Col xs="auto"><a onClick={() => handleNavLink('/')}>Category 7</a></Col>
      </Row>
    </Container>
  );
}