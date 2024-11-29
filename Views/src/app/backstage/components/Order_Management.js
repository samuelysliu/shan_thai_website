"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Table, Button, Form, InputGroup, Modal } from "react-bootstrap";
import Sidebar from "./Sidebar";
import config from "../../config";

export default function OrderManagement() {
  const endpoint = config.apiBaseUrl;

  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);

  // 控制彈出視窗顯示
  const [showModal, setShowModal] = useState(false);
  const [showAddOrderModal, setShowAddOrderModal] = useState(false);
  const [currentOrder, setCurrentOrder] = useState(null);

  const [newOrder, setNewOrder] = useState({
    uid: "",
    pid: "",
    productNumber: "",
    productPrice: 0,
    totalAmount: 0,
    discountPrice: 0,
    useDiscount: false,
    status: "待出貨",
  });

  // 獲取訂單列表和選單資料
  useEffect(() => {
    fetchOrders();
    fetchProducts();
    fetchCustomers();
  }, []);

  // 取得訂單列表
  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${endpoint}/backstage/v1/orders`);
      setOrders(response.data);
    } catch (error) {
      console.error("無法拉取訂單資料：", error);
    } finally {
      setLoading(false);
    }
  };

  // 取得產品下拉選單
  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${endpoint}/backstage/v1/product_list`);
      console.log(response.data)
      setProducts(response.data);
    } catch (error) {
      console.error("無法拉取產品資料：", error);
    }
  };

  // 取得客戶下拉選單
  const fetchCustomers = async () => {
    try {
      const response = await axios.get(`${endpoint}/backstage/v1/users_list`);
      setCustomers(response.data);
    } catch (error) {
      console.error("無法拉取客戶資料：", error);
    }
  };

  // 新增訂單
  const createOrder = async () => {
    setLoading(true);
    if (newOrder != "")
      try {
        const response = await axios.post(`${endpoint}/backstage/v1/orders`, newOrder);
        setOrders((prevOrders) => [...prevOrders, response.data]);
        handleCloseAddOrderModal();
      } catch (error) {
        console.error("無法新增訂單：", error);
      } finally {
        setLoading(false);
      }
  };

  // 搜尋與篩選功能
  const handleSearch = (e) => setSearchTerm(e.target.value);
  const handleFilterChange = (e) => setFilter(e.target.value);

  const filteredOrders = orders.filter((order) => {
    return (
      (filter === "all" || order.status === filter) &&
      order.customerName.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  // 彈出視窗控制
  const handleShowModal = (order) => {
    setCurrentOrder(order);
    setShowModal(true);
  };
  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentOrder(null);
  };

  const handleShowAddOrderModal = () => setShowAddOrderModal(true);
  const handleCloseAddOrderModal = () => {
    setShowAddOrderModal(false);
    setNewOrder({
      uid: "",
      pid: "",
      productNumber: "",
      totalAmount: 0,
      discountPrice: 0,
      useDiscount: false,
      status: "待出貨",
    });
  };

  // 價格計算

  return (
    <Container fluid>
      <Row>
        <Sidebar />
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
            <Col md={2}>
              <Button
                variant="primary"
                style={{ backgroundColor: "var(--accent-color)", borderColor: "var(--accent-color)" }}
                onClick={handleShowAddOrderModal}
              >
                新增訂單
              </Button>
            </Col>
          </Row>

          {/* 訂單表格 */}
          {loading ? (
            <p>Loading...</p>
          ) : (
            <Table striped bordered hover>
              <thead style={{ backgroundColor: "var(--primary-color)", color: "var(--light-text-color)" }}>
                <tr>
                  <th>訂單編號</th>
                  <th>顧客名稱</th>
                  <th>產品名稱</th>
                  <th>訂單日期</th>
                  <th>總金額</th>
                  <th>狀態</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredOrders.map((order) => (
                  <tr key={order.id}>
                    <td>{order.id}</td>
                    <td>{order.customerName}</td>
                    <td>{order.productName}</td>
                    <td>NT. {order.total}</td>
                    <td>{order.status}</td>
                    <td>
                      <Button
                        variant="link"
                        style={{ color: "var(--accent-color)" }}
                        onClick={() => handleShowModal(order)}
                      >
                        查看
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
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
              <p><strong>產品名稱：</strong> {currentOrder.productName}</p>
              <p><strong>訂單日期：</strong> {currentOrder.date}</p>
              <p><strong>總金額：</strong> NT. {currentOrder.total}</p>
              <p><strong>狀態：</strong> {currentOrder.status}</p>
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            關閉
          </Button>
        </Modal.Footer>
      </Modal>

      {/* 新增訂單的彈出視窗 */}
      <Modal show={showAddOrderModal} onHide={handleCloseAddOrderModal}>
        <Modal.Header closeButton>
          <Modal.Title>新增訂單</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            {/* 顧客名稱 */}
            <Form.Group className="mb-3">
              <Form.Label>顧客名稱</Form.Label>
              <Form.Select
                value={newOrder.uid}
                required
                onChange={(e) => {
                  const selecteduid = e.target.value;
                  const selectedCustomer = customers.find((customer) => customer.uid === parseInt(selecteduid));
                  setNewOrder({
                    ...newOrder,
                    uid: selecteduid,
                    customerName: selectedCustomer?.username || "",
                    customerEmail: selectedCustomer?.email || "",
                  });
                }}
              >
                <option value="">選擇顧客</option>
                {customers.map((customer) => (
                  <option key={customer.uid} value={customer.uid}>
                    {customer.username}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            {/* 顧客 Email */}
            <Form.Group className="mb-3">
              <Form.Label>顧客 Email</Form.Label>
              <Form.Control
                type="email"
                value={newOrder.customerEmail || ""}
                disabled
              />
            </Form.Group>

            {/* 產品名稱 */}
            <Form.Group className="mb-3">
              <Form.Label>產品名稱</Form.Label>
              <Form.Select
                value={newOrder.pid}
                required
                onChange={(e) => {
                  const selectedPid = e.target.value;
                  const selectedProduct = products.find(
                    (product) => product.pid === parseInt(selectedPid)
                  );
                  setNewOrder({
                    ...newOrder,
                    pid: selectedPid,
                    productPrice: selectedProduct?.price || 0,
                    totalAmount: (selectedProduct?.price || 0) * newOrder.productNumber,
                  });
                }}
              >
                <option value="">選擇產品</option>
                {products.map((product) => (
                  <option key={product.pid} value={product.pid}>
                    {product.title_cn}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            {/* 下單數量 */}
            <Form.Group className="mb-3">
              <Form.Label>數量</Form.Label>
              <Form.Control
                type="number"
                value={newOrder.productNumber || 1}
                required
                onChange={(e) => {
                  const quantity = parseInt(e.target.value) || 1;
                  setNewOrder({
                    ...newOrder,
                    productNumber: quantity,
                    totalAmount: quantity * newOrder.productPrice,
                  });
                }}
              />
            </Form.Group>

            {/* 總金額 */}
            <Form.Group className="mb-3">
              <Form.Label>總金額</Form.Label>
              <Form.Control
                type="number"
                value={newOrder.totalAmount || 0}
                disabled={true}
              />
            </Form.Group>

            {/* 優惠價 */}
            <Form.Group className="mb-3">
              <Form.Check
                type="checkbox"
                label="是否使用優惠價"
                checked={newOrder.useDiscount || false}
                onChange={(e) =>
                  setNewOrder({ ...newOrder, useDiscount: e.target.checked })
                }
              />
              {newOrder.useDiscount && (
                <Form.Control
                  className="mt-2"
                  type="number"
                  value={newOrder.discountPrice || 0}
                  onChange={(e) =>
                    setNewOrder({ ...newOrder, discountPrice: parseInt(e.target.value) || 0 })
                  }
                />
              )}
            </Form.Group>

            {/* 訂單狀態 */}
            <Form.Group className="mb-3">
              <Form.Label>狀態</Form.Label>
              <Form.Select
                value={newOrder.status}
                required
                onChange={(e) => setNewOrder({ ...newOrder, status: e.target.value })}
              >
                <option value="待出貨">待出貨</option>
                <option value="已出貨">已出貨</option>
                <option value="已取消">已取消</option>
              </Form.Select>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseAddOrderModal}>
            取消
          </Button>
          <Button
            variant="primary"
            style={{
              backgroundColor: "var(--accent-color)",
              borderColor: "var(--accent-color)",
            }}
            onClick={createOrder}
          >
            新增
          </Button>
        </Modal.Footer>
      </Modal>


    </Container>
  );
}
