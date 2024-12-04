"use client";  // 設定為客戶端組件

import React from "react";
import { Container, Row, Col } from 'react-bootstrap';

export default function Product_Menu({ productTags, onTagSelect }) {

  return (
    <Container fluid className="product-menu-container">
      <Row className="product-menu">
        <Col key={-1} className="tag-item" xs="auto">
          <a onClick={() => onTagSelect(-1)}>全部</a>
        </Col>
        {productTags.map((tag) => (
          <Col key={tag.ptid} className="tag-item" xs="auto">
            <a onClick={() => onTagSelect(tag.ptid)}>{tag.productTag}</a>
          </Col>
        ))}
      </Row>
    </Container>
  );
}