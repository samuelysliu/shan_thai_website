"use client";

import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useRouter } from "next/navigation"; // 引入 useRouter
import axios from "axios";
import { Container, Row, Col, Card, Button, Spinner } from "react-bootstrap";
import config from "../config";
import { setProducts } from "../redux/slices/productSlice";

const Product_Grid = () => {
  let endpoint = config.apiBaseUrl;
  const dispatch = useDispatch();
  const products = useSelector((state) => state.product.products); // 從 Redux Store 獲取產品列表
  const router = useRouter(); // 初始化 router

  const [loading, setLoading] = useState(true); // 用於顯示加載狀態
  const [error, setError] = useState(null); // 用於顯示錯誤訊息

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await axios.get(endpoint + "/frontstage/v1/product"); // API 路徑
      dispatch(setProducts(response.data)); // 儲存到 Redux Store
    } catch (err) {
      setError("無法加載產品清單，請稍後再試。");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="text-center my-4">
        <p className="text-danger">{error}</p>
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