// src/app/components/OrderManagement.js
"use client";

import React, { useState } from 'react';
import { Container, Row, Col, Table, Button, Form, InputGroup, Modal } from 'react-bootstrap';
import Sidebar from './Sidebar';

export default function OrderManagement() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");
  const [orders, setOrders] = useState([
    { id: 1, customerName: "顧客A", date: "2024-11-01", total: 1500, status: "待出貨" },
    { id: 2, customerName: "顧客B", date: "2024-11-02", total: 2500, status: "已出貨" },
    { id: 3, customerName: "顧客C", date: "2024-11-03", total: 750, status: "已取消" },
    // 更多訂單資料...
  ]);

  const [showModal, setShowModal] = useState(false);
  const [currentOrder, setCurrentOrder] = useState(null);

  const handleSearch = (e) => setSearchTerm(e.target.value);
  const handleFilterChange = (e) => setFilter(e.target.value);

  const handleShowModal = (order) => {
    setCurrentOrder(order);
    setShowModal(true);
  };
  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentOrder(null);
  };

  const filteredOrders = orders.filter(order => {
    return (
      (filter === "all" || order.status === filter) &&
      order.customerName.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  return (
    <Container fluid>
      <Row>
        <Sidebar />
        {/* 主要內容 */}
        <Col xs={10} className="p-4">
          <h3 className="mb-4" style={{ color: "var(--primary-color)" }}>訂單管理</h3>
          
          {/* 搜尋和篩選 */}
          <Row className="mb-3">
            <Col md={6}>
              <InputGroup>
                <Form.Control
                  placeholder="搜尋顧客名稱"
                  value={searchTerm}
                  onChange={handleSearch}
                />
              </InputGroup>
            </Col>
            <Col md={4}>
              <Form.Select onChange={handleFilterChange} value={filter}>
                <option value="all">所有狀態</option>
                <option value="待出貨">待出貨</option>
                <option value="已出貨">已出貨</option>
                <option value="已取消">已取消</option>
              </Form.Select>
            </Col>
          </Row>

          {/* 訂單表格 */}
          <Table striped bordered hover>
            <thead style={{ backgroundColor: "var(--primary-color)", color: "var(--light-text-color)" }}>
              <tr>
                <th>訂單編號</th>
                <th>顧客名稱</th>
                <th>訂單日期</th>
                <th>總金額</th>
                <th>狀態</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {filteredOrders.map(order => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.customerName}</td>
                  <td>{order.date}</td>
                  <td>NT. {order.total}</td>
                  <td>{order.status}</td>
                  <td>
                    <Button variant="link" style={{ color: "var(--accent-color)" }} onClick={() => handleShowModal(order)}>查看</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>

      {/* 訂單詳細資訊的彈出視窗 */}
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>訂單詳情</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {currentOrder && (
            <div>
              <p><strong>訂單編號：</strong> {currentOrder.id}</p>
              <p><strong>顧客名稱：</strong> {currentOrder.customerName}</p>
              <p><strong>訂單日期：</strong> {currentOrder.date}</p>
              <p><strong>總金額：</strong> NT. {currentOrder.total}</p>
              <p><strong>狀態：</strong> {currentOrder.status}</p>
              {/* 可以在這裡顯示更多訂單詳細資訊 */}
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            關閉
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}
