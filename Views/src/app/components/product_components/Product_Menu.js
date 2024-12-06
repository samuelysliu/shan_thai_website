"use client";  // 設定為客戶端組件

import React, {useState} from "react";
import { Container, Row, Col } from 'react-bootstrap';

export default function Product_Menu({ productTags, onTagSelect }) {
  const [selectedTag, setSelectedTag] = useState(-1); // 用於追踪當前選中的標籤

  // 當點擊標籤時處理選擇
  const handleTagSelect = (ptid) => {
    setSelectedTag(ptid); // 更新選中的標籤
    onTagSelect(ptid); // 調用父組件的回調函數
  };

  return (
    <Container fluid className="product-menu-container">
      <Row className="product-menu">
        <Col key={-1} className="tag-item" xs="auto">
          <a
            onClick={() => handleTagSelect(-1)}
            className={selectedTag === -1 ? "selected-tag" : ""}
          >
            全部
          </a>
        </Col>
        {productTags.map((tag) => (
          <Col key={tag.ptid} className="tag-item" xs="auto">
            <a
              onClick={() => handleTagSelect(tag.ptid)}
              className={selectedTag === tag.ptid ? "selected-tag" : ""}
            >
              {tag.productTag}
            </a>
          </Col>
        ))}
      </Row>
    </Container>
  );
}