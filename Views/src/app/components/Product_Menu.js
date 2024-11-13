"use client";  // 設定為客戶端組件

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

export default function Product_Menu() {
    return (
      <Container fluid>
        <Row className="product_menu">
          <Col xs="auto"><a href="/category/1">Category 1</a></Col>
          <Col xs="auto"><a href="/category/2">Category 2</a></Col>
          <Col xs="auto"><a href="/category/3">Category 3</a></Col>
          <Col xs="auto"><a href="/category/4">Category 4</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          <Col xs="auto"><a href="/category/5">Category 5</a></Col>
          
        </Row>
      </Container>
    );
  }