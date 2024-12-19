"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Card, Badge, Button, Modal, Spinner } from "react-bootstrap";
import config from "../../config";
import { useSelector, useDispatch } from "react-redux";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示
import { useRouter } from "next/navigation";

import { showToast } from "@/app/redux/slices/toastSlice";

const OrderHistory = () => {
  const endpoint = config.apiBaseUrl;
  const router = useRouter();

  const [orders, setOrders] = useState([]); // 訂單列表
  const [loading, setLoading] = useState(true); // 加載狀態
  const [error, setError] = useState(null); // 錯誤訊息
  const [showModal, setShowModal] = useState(false); // 控制彈出視窗
  const [selectedOrderId, setSelectedOrderId] = useState(null); // 被選中的訂單 ID

  const { token, userInfo } = useSelector((state) => state.user); // 從 Redux 獲取使用者資訊與 Token
  const dispatch = useDispatch();

  useEffect(() => {
    fetchOrders();
  }, [userInfo, token]);

  // 取得所有訂單 API
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
      const response = await axios.delete(`${endpoint}/frontstage/v1/orders/${orderId}`, {
        headers: {
          Authorization: `Bearer ${token}`, // 請替換成正確的 Token
        },
      });
      handleSuccess("訂單已成功取消");

      fetchOrders();
    } catch (err) {
      console.error("取消訂單失敗：", err);
      handleError("取消訂單失敗，請稍後再試。");
    } finally {
      setShowModal(false); // 關閉彈出視窗
    }
  };

  // 更新訂單 API
  const updateOrder = async (orderId) => {
    try {
      const response = await axios.put(`${endpoint}/frontstage/v1/orders/${orderId}`, { "status": "待確認" }, {
        headers: {
          Authorization: `Bearer ${token}`, // 請替換成正確的 Token
        },
      });

      fetchOrders();
    } catch (err) {
      console.error("更新訂單失敗：", err);
    } finally {
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

  // 控制彈出視窗訊息區
  const handleSuccess = (message) => {
    dispatch(showToast({ message: message, variant: "success" }));
  };

  const handleError = (message) => {
    dispatch(showToast({ message: message, variant: "danger" }));
  };

  return (
    <Container className="my-4">
      <Row className="my-3">
        <Col xs={12}>
          <Button variant="link" onClick={() => router.push("/")}>
            <FaArrowLeft /> 返回
          </Button>
        </Col>
      </Row>
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

                  <div>
                    <strong>訂單狀態:</strong>{" "}
                    <Badge
                      bg={
                        order.status === "已完成"
                          ? "success"
                          : order.status === "送貨中"
                            ? "warning"
                            : order.status === "待出貨"
                              ? "primary"
                              : order.status === "取消"
                                ? "secondary"
                                : "danger"
                      }
                    >
                      {order.status}
                    </Badge>
                  </div>
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
                {(order.paymentMethod === "匯款" && order.status === "待匯款") &&
                  <>
                    < div >
                      <strong>銀行代號：</strong>001 <strong>匯款帳號：</strong>123456 { }
                      <Button onClick={() => { updateOrder(order.oid) }}>
                        我已匯款，通知管理員
                      </Button>
                    </div>
                    <hr />
                  </>
                }

                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <strong>總價:</strong> NT. {order.totalAmount}
                  </div>

                  {/* 如果狀態是 "待出貨"、"待確認"，顯示 X 按鈕 */}
                  {(order.status === "待出貨" || order.status === "待匯款") && (
                    <Button
                      variant="link"
                      className="text-danger"
                      onClick={() => handleShowModal(order.oid)}
                    >
                      取消訂單
                    </Button>
                  )}
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
    </Container >

  );
};

export default OrderHistory;
