"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Table, Button, Form, InputGroup, Modal } from "react-bootstrap";
import Sidebar from "./Sidebar";
import config from "../../config";

import { useSelector } from 'react-redux';

export default function OrderManagement() {
  const endpoint = config.apiBaseUrl;

  // 從 Redux 中取出會員資訊
  const { token } = useSelector((state) => state.user);

  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);

  // 控制彈出視窗顯示
  const [showOrderModal, setShowOrderModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false); // 區分新增與編輯模式

  const [newOrder, setNewOrder] = useState({
    oid: "",
    uid: "",
    pid: "",
    productNumber: 1,
    productPrice: 0,
    totalAmount: 0,
    discountPrice: 0,
    useDiscount: false,
    address: "",
    transportationMethod: "Seven 店到店",
    status: "待出貨",
  });

  useEffect(() => {
    fetchOrders();
    fetchProducts();
    fetchCustomers();
  }, []);

  // 拉取所有訂單
  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${endpoint}/backstage/v1/orders`, {
        headers: {
            Authorization: `Bearer ${token}`,
        }
    });
      setOrders(response.data);
    } catch (error) {
      console.error("無法拉取訂單資料：", error);
    } finally {
      setLoading(false);
    }
  };

  // 拉取產品清單
  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${endpoint}/backstage/v1/product_list`, {
        headers: {
            Authorization: `Bearer ${token}`,
        }
    });
      setProducts(response.data);
    } catch (error) {
      console.error("無法拉取產品資料：", error);
    }
  };

  // 拉取客戶清單
  const fetchCustomers = async () => {
    try {
      const response = await axios.get(`${endpoint}/backstage/v1/users_list`, {
        headers: {
            Authorization: `Bearer ${token}`,
        }
    });
      setCustomers(response.data);
    } catch (error) {
      console.error("無法拉取客戶資料：", error);
    }
  };

  // 控制新增或編輯訂單的變數初始值
  const handleShowOrderModal = (order = null) => {
    if (order) {
      setNewOrder({
        oid: order.oid,
        uid: order.uid,
        pid: order.pid,
        productNumber: order.productNumber,
        productPrice: order.productPrice,
        totalAmount: order.totalAmount,
        discountPrice: order.discountPrice,
        useDiscount: order.discountPrice > 0,
        address: order.address,
        transportationMethod: order.transportationMethod,
        status: order.status,
      });
      setIsEditing(true);
    } else {
      setNewOrder({
        oid: "",
        uid: "",
        pid: "",
        productNumber: 1,
        productPrice: 0,
        totalAmount: 0,
        discountPrice: 0,
        useDiscount: false,
        address: "",
        transportationMethod: "Seven 店到店",
        status: "待出貨",
      });
      setIsEditing(false);
    }
    setShowOrderModal(true);
  };

  const handleCloseOrderModal = () => {
    setShowOrderModal(false);
    setIsEditing(false);
  };

  //新增訂單
  const createOrder = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${endpoint}/backstage/v1/orders`, newOrder, {
        headers: {
            Authorization: `Bearer ${token}`,
        }
    });

      const newOrderData = response.data;
      newOrderData.username = newOrder.customerName;
      let selectedProduct = products.find(
        (product) => product.pid === parseInt(newOrder.pid)
      );
      newOrderData.productTitle_cn = selectedProduct.title_cn;

      setOrders((prevOrders) => [...prevOrders, newOrderData]);
      handleCloseOrderModal();
    } catch (error) {
      console.error("無法新增訂單：", error);
    } finally {
      setLoading(false);
    }
  };

  // 編輯訂單
  const updateOrder = async () => {
    setLoading(true);
    try {
      let requestData = {
        productNumber: newOrder.productNumber,
        totalAmount: newOrder.totalAmount,
        discountPrice: newOrder.discountPrice,
        useDiscount: newOrder.useDiscount,
        address: newOrder.address,
        transportationMethod: newOrder.transportationMethod,
        status: newOrder.status,
      }

      const response = await axios.patch(`${endpoint}/backstage/v1/orders/${newOrder.oid}`, requestData, {
        headers: {
            Authorization: `Bearer ${token}`,
        }
    });

      const newOrderData = response.data;

      let selectedCustomer = customers.find((customer) => customer.uid === parseInt(newOrder.uid));
      newOrderData.username = selectedCustomer.username;
      let selectedProduct = products.find(
        (product) => product.pid === parseInt(newOrder.pid)
      );
      newOrderData.productTitle_cn = selectedProduct.title_cn;

      setOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.oid === newOrder.oid ? { ...order, ...newOrderData } : order
        )
      );
      handleCloseOrderModal();
    } catch (error) {
      console.error("無法更新訂單：", error);
    } finally {
      setLoading(false);
    }
  };

  // 控制表單送出是要新增還是編輯訂單
  const handleSubmit = () => {
    if (isEditing) {
      updateOrder();
    } else {
      createOrder();
    }
  };

  // 搜尋與篩選功能
  const handleSearch = (e) => setSearchTerm(e.target.value);
  const handleFilterChange = (e) => setFilter(e.target.value);

  const filteredOrders = orders.filter((order) => {
    const username = order.username || ""; // 確保 username 為空字串而非 null
    return (
      (filter === "all" || order.status === filter) &&
      username.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  return (
    <Container fluid>
      <Row>
        <Sidebar />
        <Col xs={10} className="p-4">
          <h3 className="mb-4" style={{ color: "var(--primary-color)" }}>訂單管理</h3>
          <Row className="mb-3">
            <Col md={6}>
              <InputGroup>
                <Form.Control
                  placeholder="搜尋客戶名稱"
                  value={searchTerm}
                  onChange={handleSearch}
                />
              </InputGroup>
            </Col>
            <Col md={4}>
              <Form.Select value={filter} onChange={handleFilterChange}>
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
                onClick={() => handleShowOrderModal()}
              >
                新增訂單
              </Button>
            </Col>
          </Row>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>訂單編號</th>
                  <th>客戶名稱</th>
                  <th>產品名稱</th>
                  <th>總金額</th>
                  <th>狀態</th>
                  <th>訂單日期</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredOrders.map((order) => (
                  <tr key={order.oid}>
                    <td>{order.oid}</td>
                    <td>{order.username}</td>
                    <td>{order.productTitle_cn}</td>
                    <td>{order.totalAmount}</td>
                    <td>{order.status}</td>
                    <td>{order.created_at}</td>
                    <td>
                      <Button
                        variant="link"
                        style={{ color: "var(--accent-color)" }}
                        onClick={() => handleShowOrderModal(order)}
                      >
                        編輯
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Col>
      </Row>

      {/* 訂單彈出視窗 */}
      <Modal show={showOrderModal} onHide={handleCloseOrderModal}>
        <Modal.Header closeButton>
          <Modal.Title>{isEditing ? "編輯訂單" : "新增訂單"}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            {/* 客戶名稱 */}
            <Form.Group className="mb-3">
              <Form.Label>客戶名稱</Form.Label>
              <Form.Select
                value={newOrder.uid}
                required
                onChange={(e) => {
                  const selectedUid = e.target.value;
                  const selectedCustomer = customers.find((customer) => customer.uid === parseInt(selectedUid));
                  setNewOrder({
                    ...newOrder,
                    uid: selectedUid,
                    customerName: selectedCustomer?.username || "",
                    customerEmail: selectedCustomer?.email || "",
                  });
                }}
                disabled={isEditing}
              >
                <option value="">選擇客戶</option>
                {customers.map((customer) => (
                  <option key={customer.uid} value={customer.uid}>
                    {customer.username}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            {/* 客戶 Email */}
            <Form.Group className="mb-3">
              <Form.Label>客戶 Email</Form.Label>
              <Form.Select
                value={newOrder.customerEmail}
                required
                onChange={(e) => {
                  const selectedEmail = e.target.value;
                  const selectedCustomer = customers.find((customer) => customer.email === selectedEmail);
                  setNewOrder({
                    ...newOrder,
                    uid: selectedCustomer?.uid || "",
                    customerName: selectedCustomer?.username || "",
                    customerEmail: selectedEmail,
                  });
                }}
                disabled={isEditing}
              >
                <option value="">選擇 Email</option>
                {customers.map((customer) => (
                  <option key={customer.uid} value={customer.email}>
                    {customer.email}
                  </option>
                ))}
              </Form.Select>
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
                disabled={isEditing}
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
                <option value="已完成">已完成</option>
                <option value="已取消">已取消</option>
              </Form.Select>
            </Form.Group>

            {/* 貨運方式 */}
            <Form.Group className="mb-3">
              <Form.Label>貨運方式</Form.Label>
              <Form.Select
                value={newOrder.transportationMethod}
                required
                onChange={(e) => setNewOrder({ ...newOrder, transportationMethod: e.target.value })}
              >
                <option value="Seven 店到店">Seven 店到店</option>
                <option value="全家 店到">全家 店到店</option>
                <option value="宅配">宅配</option>
              </Form.Select>
            </Form.Group>

            {/* 運送地址 */}
            <Form.Group className="mb-3">
              <Form.Label>地址或超商店名</Form.Label>
              <Form.Control
                type="string"
                value={newOrder.address}
                required
                onChange={(e) => setNewOrder({ ...newOrder, address: e.target.value })}
              />
            </Form.Group>
          </Form>

        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseOrderModal}>
            取消
          </Button>
          <Button
            variant="primary"
            style={{ backgroundColor: "var(--accent-color)", borderColor: "var(--accent-color)" }}
            onClick={handleSubmit}
          >
            {isEditing ? "儲存" : "新增"}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}
