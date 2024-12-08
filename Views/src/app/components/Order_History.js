"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Card, Badge, Button, Modal, Spinner } from "react-bootstrap";
import { FaTimes } from "react-icons/fa";
import config from "../config";
import { useSelector } from "react-redux";

const OrderHistory = () => {
  const endpoint = config.apiBaseUrl;

  const [orders, setOrders] = useState([]); // 訂單列表
  const [loading, setLoading] = useState(true); // 加載狀態
  const [error, setError] = useState(null); // 錯誤訊息
  const [showModal, setShowModal] = useState(false); // 控制彈出視窗
  const [selectedOrderId, setSelectedOrderId] = useState(null); // 被選中的訂單 ID

  const { token, userInfo } = useSelector((state) => state.user); // 從 Redux 獲取使用者資訊與 Token

  useEffect(() => {
    fetchOrders();
  }, [userInfo, token]);

  // 新增訂單 API
  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${endpoint}/frontstage/v1/orders?uid=${userInfo.uid}`, // API 路徑加上用戶 ID
        {
          headers: {
            Authorization: `Bearer ${token}`, // 加入 Authorization header
          },
        }
      );
      setOrders(response.data); // 更新訂單列表
    } catch (err) {
      setError("無法加載訂單資料，請稍後再試。");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // 刪除訂單 API
  const cancelOrder = async (orderId) => {
    try {
      await axios.delete(`${endpoint}/frontstage/v1/orders/${orderId}`, {
        headers: {
          Authorization: `Bearer ${token}`, // 請替換成正確的 Token
        },
      });
      alert("訂單已成功取消");
      fetchOrders(); // 刷新訂單列表
    } catch (err) {
      console.error("取消訂單失敗：", err);
      alert("取消訂單失敗，請稍後再試。");
    } finally {
      setShowModal(false); // 關閉彈出視窗
    }
  };

  const handleShowModal = (orderId) => {
    setSelectedOrderId(orderId);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setSelectedOrderId(null);
    setShowModal(false);
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
        <Alert variant="danger">{error}</Alert>
      </Container>
    );
  }

  if (orders.length === 0) {
    return (
      <Container className="text-center my-4">
        <Alert variant="info">目前沒有任何訂單。</Alert>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <h2 className="mb-4">我的訂單</h2>
      <Row className="gy-4">
        {orders.map((order) => (
          <Col xs={12} key={order.oid}>
            <Card className="order-card">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center">
                  <Card.Title className="mb-3">
                    訂單編號: <strong>{order.oid}</strong>
                  </Card.Title>
                  {/* 如果狀態是 "待出貨"，顯示 X 按鈕 */}
                  {order.status === "待出貨" && (
                    <Button
                      variant="link"
                      className="text-danger"
                      onClick={() => handleShowModal(order.oid)}
                    >
                      <FaTimes size={20} />
                    </Button>
                  )}
                </div>
                <Card.Text>
                  <strong>訂單日期:</strong> {order.created_at}
                </Card.Text>
                <hr />
                <div>
                  {order.details.map((product, index) => (
                    <Row key={index} className="align-items-center mb-3">
                      <Col xs={12} md={4} className="text-center">
                        <img
                          src={product.productImageUrl}
                          alt={product.title_cn}
                          className="product-image"
                          width={200}
                        />
                      </Col>
                      <Col xs={12} md={8}>
                        <strong>{product.title_cn}</strong> x {product.quantity} <br />
                        單價: NT. {product.price} <br />
                        總價: NT. {product.price * product.quantity}
                      </Col>
                    </Row>
                  ))}
                </div>
                <hr />
                <div>
                  <strong>總價:</strong> NT. {order.totalAmount}
                </div>
                <div className="mt-3">
                  <strong>訂單狀態:</strong>{" "}
                  <Badge
                    bg={
                      order.status === "completed"
                        ? "success"
                        : order.status === "processing"
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

      {/* 確認刪除的彈出視窗 */}
      <Modal show={showModal} onHide={handleCloseModal} centered>
        <Modal.Header closeButton>
          <Modal.Title>確認取消訂單</Modal.Title>
        </Modal.Header>
        <Modal.Body>您確定要取消這筆訂單嗎？此操作無法恢復。</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            取消
          </Button>
          <Button
            variant="danger"
            onClick={() => cancelOrder(selectedOrderId)}
          >
            確認取消
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>

  );
};

export default OrderHistory;
