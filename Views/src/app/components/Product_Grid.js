"use client";

import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useRouter } from "next/navigation"; // 引入 useRouter
import axios from "axios";
import { Container, Row, Col, Card, Button, Spinner } from "react-bootstrap";
import config from "../config";

import { setProducts } from "../redux/slices/productSlice";

const Product_Grid = ({ initialProducts }) => {
  let endpoint = config.apiBaseUrl;
  const dispatch = useDispatch();
  const router = useRouter();

  useEffect(() => {
    if (initialProducts.length > 0) {
      dispatch(setProducts(initialProducts));
    }
  }, [initialProducts, dispatch]);

  const storedProducts = useSelector((state) => state.product.products); // 從 Redux Store 獲取產品列表
  const products = storedProducts.length > 0 ? storedProducts : initialProducts

  if (!products || products.length === 0) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品...</p>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <Row xs={2} md={3} xl={4} xxl={5}>
        {products.map((product) => (
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