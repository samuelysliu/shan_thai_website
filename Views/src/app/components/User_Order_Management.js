"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Card, Badge, Spinner } from "react-bootstrap";
import config from "../config";

const UserOrderManagement = () => {
  const endpoint = config.apiBaseUrl;

  const [orders, setOrders] = useState([]); // 訂單列表
  const [loading, setLoading] = useState(true); // 加載狀態
  const [error, setError] = useState(null); // 錯誤訊息

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${endpoint}/frontstage/v1/orders`); // 替換為實際 API 路徑
      setOrders(response.data); // 更新訂單列表
    } catch (err) {
      setError("無法加載訂單資料，請稍後再試。");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載訂單...</p>
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
      <Row>
        {orders.map((order) => (
          <Col xs={12} md={6} lg={4} key={order.orderId} className="mb-4">
            <Card className="order-card">
              <Card.Body>
                <Card.Title className="mb-2">
                  訂單編號: <strong>{order.orderId}</strong>
                </Card.Title>
                <Card.Text>
                  <strong>訂單日期:</strong> {order.orderDate}
                </Card.Text>
                <hr />
                <div>
                  {order.products.map((product, index) => (
                    <div key={index} className="mb-2">
                      <strong>{product.name}</strong> x {product.quantity} <br />
                      單價: NT. {product.price}
                    </div>
                  ))}
                </div>
                <hr />
                <div>
                  <strong>總價:</strong> NT. {order.totalPrice}
                </div>
                <div>
                  <strong>訂單狀態:</strong>{" "}
                  <Badge
                    bg={
                      order.status === "已完成"
                        ? "success"
                        : order.status === "處理中"
                        ? "warning"
                        : "danger"
                    }
                  >
                    {order.status}
                  </Badge>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default UserOrderManagement;
