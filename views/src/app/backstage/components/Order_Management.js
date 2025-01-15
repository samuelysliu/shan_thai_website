// src/app/components/Order_Management.js
"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Table, Button, Form, InputGroup, Modal } from "react-bootstrap";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import Sidebar from "./Sidebar";
import config from "../../config";

import { useSelector, useDispatch } from 'react-redux';

import { createLogisticCheckMacValue } from "../../components/Tools";

import { showToast } from "@/app/redux/slices/toastSlice";

export default function OrderManagement() {
  const endpoint = config.apiBaseUrl;

  // 從 Redux 中取出會員資訊
  const { token } = useSelector((state) => state.user);

  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");
  const [orders, setOrders] = useState([]);
  const [expandedRows, setExpandedRows] = useState([]); // 存儲展開的訂單編號
  const [loading, setLoading] = useState(true);

  const dispatch = useDispatch();

  // 控制彈出視窗顯示
  const [showOrderModal, setShowOrderModal] = useState(false);

  const [editableOrder, setEditableOrder] = useState({
    oid: "",
    recipientName: "",
    recipientPhone: "",
    recipientEmail: "",
    address: "",
    transportationMethod: "",
    note: "",
    status: "",
    useDiscount: false,
    discountPrice: 0,
    totalAmount: 0,
  });

  useEffect(() => {
    fetchOrders();
  }, []);

  // 拉取所有訂單
  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${endpoint}/backstage/v1/orders`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setOrders(response.data);
    } catch (error) {
      console.error("無法拉取訂單資料：", error);
    } finally {
      setLoading(false);
    }
  };

  // 切換展開行
  const toggleRow = (oid) => {
    if (expandedRows.includes(oid)) {
      setExpandedRows(expandedRows.filter((rowId) => rowId !== oid));
    } else {
      setExpandedRows([...expandedRows, oid]);
    }
  };


  // 控制彈出視窗
  const handleShowOrderModal = (order) => {
    setEditableOrder({
      oid: order.oid,
      recipientName: order.recipientName || "",
      recipientPhone: order.recipientPhone || "",
      recipientEmail: order.recipientEmail || "",
      address: order.address || "",
      transportationMethod: order.transportationMethod || "delivery",
      note: order.note || "",
      status: order.status || "待出貨",
      useDiscount: order.useDiscount || false,
      discountPrice: order.discountPrice || 0,
      totalAmount: order.totalAmount || 0,
    });
    setShowOrderModal(true);
  };

  // 更新訂單
  const updateOrder = async () => {
    setLoading(true);
    try {
      const requestData = {
        recipientName: editableOrder.recipientName,
        recipientPhone: editableOrder.recipientPhone,
        recipientEmail: editableOrder.recipientEmail,
        address: editableOrder.address,
        transportationMethod: editableOrder.transportationMethod,
        note: editableOrder.note,
        status: editableOrder.status,
        useDiscount: editableOrder.useDiscount,
        discountPrice: editableOrder.discountPrice,
      };

      const response = await axios.patch(
        `${endpoint}/backstage/v1/orders/${editableOrder.oid}`,
        requestData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const updatedOrder = response.data;

      setOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.oid === updatedOrder.oid ? { ...order, ...updatedOrder } : order
        )
      );

      setShowOrderModal(false);
    } catch (error) {
      console.error("無法更新訂單：", error);
    } finally {
      setLoading(false);
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

  // 建立物流訂單
  const createLogistic = async (oid) => {
    await axios.post(
      `${endpoint}/backstage/v1/create_logistics/${oid}`, {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
  }

  // 列印託運單功能
  const printLogistic = async (order) => {
    try {
      const logisticOrder = await axios.get(`${endpoint}/backstage/v1/logistic_print/${order.oid}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      });

      let params = {};
      let printEndpoint = ""

      // 處理 seven 的託運單
      if (order.transportationMethod === "seven") {
        params = {
          MerchantID: logisticOrder.data.MerchantID, // 特店編號
          AllPayLogisticsID: logisticOrder.data.AllPayLogisticsID, // 物流交易編號
          CVSPaymentNo: logisticOrder.data.CVSPaymentNo, // 寄貨編號
          CVSValidationNo: logisticOrder.data.CVSValidationNo // 驗證碼
        };

        printEndpoint = config.sevenPrintEndpoint;

      } else if (order.transportationMethod === "family") { // 處理 family 的托運單
        params = {
          MerchantID: logisticOrder.data.MerchantID, // 特店編號
          AllPayLogisticsID: logisticOrder.data.AllPayLogisticsID, // 物流交易編號
          CVSPaymentNo: logisticOrder.data.CVSPaymentNo, // 寄貨編號
        };

        printEndpoint = config.familyPrintEndpoint;

      } else {
        params = {
          MerchantID: logisticOrder.data.MerchantID, // 特店編號
          AllPayLogisticsID: logisticOrder.data.AllPayLogisticsID, // 物流交易編號
          PrintMode: 1  //列印模式， 1：使用一般模式(A4 大小)；2：使用熱感應標籤機模式(A6 大小)
        };

        printEndpoint = config.deliveryPrintEndpoint;

      }
      const CheckMacValue = createLogisticCheckMacValue(params)
      // 添加 CheckMacValue 到表單數據
      params.CheckMacValue = CheckMacValue;
      console.log(params)

      const popupWindow = window.open("", "printWindow", "width=800,height=600,scrollbars=no,resizable=no");
      // 建立隱藏的表單
      const form = document.createElement("form");
      form.method = "POST";
      form.action = printEndpoint;
      form.target = "printWindow";

      // 將參數加入表單
      Object.entries(params).forEach(([key, value]) => {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = key;
        input.value = value;
        form.appendChild(input);
      });

      // 提交表單
      document.body.appendChild(form);
      form.submit();
      document.body.removeChild(form); // 提交後刪除表單
    }
    catch (err) {
      createLogistic(order.oid);
      handleError("物流單不存在，正在自動建立中。請等 30 秒後再試，如果仍看到此訊息，請前往綠界後台列印託運單");
    }
  }



  // 控制彈出視窗訊息區
  const handleSuccess = (message) => {
    dispatch(showToast({ message: message, variant: "success" }));
  };

  const handleError = (message) => {
    dispatch(showToast({ message: message, variant: "danger" }));
  };

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
                <option value="待確認">待確認</option>
                <option value="待出貨">待出貨</option>
                <option value="已出貨">已出貨</option>
                <option value="已完成">已完成</option>
                <option value="已取消">已取消</option>
              </Form.Select>
            </Col>
          </Row>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>訂單編號</th>
                  <th>總金額</th>
                  <th>收件人姓名</th>
                  <th>運輸方式</th>
                  <th>付款方式</th>
                  <th>狀態</th>
                  <th>成立時間</th>
                  <th>展開</th>
                  <th>編輯</th>
                  <th>出貨單</th>
                </tr>
              </thead>
              <tbody>
                {filteredOrders.map((order) => (
                  <React.Fragment key={order.oid}>
                    <tr>
                      <td>{order.oid}</td>
                      <td>NT. {order.totalAmount}</td>
                      {/*<td>{order.useDiscount ? <>NT. {order.discountPrice}</> : "無"}</td>*/}
                      <td>{order.recipientName}</td>
                      <td>{
                        order.transportationMethod == "delivery" ? "宅配"
                          : (order.transportationMethod == "seven" ? "Seven 自取" : "全家自取")
                      }</td>
                      <td>{order.paymentMethod}</td>
                      <td>{order.status}</td>
                      <td>{order.created_at}</td>
                      <td>
                        <Button
                          variant="link"
                          style={{ color: "var(--accent-color)" }}
                          onClick={() => toggleRow(order.oid)}
                        >
                          {expandedRows.includes(order.oid) ? (
                            <FaChevronUp />
                          ) : (
                            <FaChevronDown />
                          )}
                        </Button>
                      </td>
                      <td>
                        <Button
                          variant="link"
                          style={{ color: "var(--accent-color)" }}
                          onClick={() => handleShowOrderModal(order)}
                        >
                          編輯
                        </Button>
                      </td>
                      <td>
                        {
                          order.status === "待出貨"
                            ? <Button
                              variant="link"
                              style={{ color: "var(--accent-color)" }}
                              onClick={() => printLogistic(order)}
                            >
                              列印
                            </Button>
                            : ""}

                      </td>
                    </tr>

                    {expandedRows.includes(order.oid) && (
                      <tr key={`${order.oid}-details`}>
                        <td colSpan="13">
                          <Table bordered size="sm">
                            <thead>
                              <tr>
                                <th>商品名稱</th>
                                <th>商品數量</th>
                                <th>單價</th>
                                <th>總額</th>
                              </tr>
                            </thead>
                            <tbody>
                              {order.details.map((detail) => (
                                <tr key={detail.pid}>
                                  <td>{detail.productTitle_cn}</td>
                                  <td>{detail.productNumber}</td>
                                  <td>NT. {detail.price}</td>
                                  <td>NT. {detail.subtotal}</td>
                                </tr>
                              ))}
                            </tbody>
                          </Table>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </Table>
          )}
        </Col>
      </Row>

      {/* 編輯訂單視窗 */}
      <Modal show={showOrderModal} onHide={() => setShowOrderModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>編輯訂單</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>收件人姓名</Form.Label>
              <Form.Control
                type="text"
                value={editableOrder.recipientName}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    recipientName: e.target.value,
                  })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>電話</Form.Label>
              <Form.Control
                type="text"
                value={editableOrder.recipientPhone}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    recipientPhone: e.target.value,
                  })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={editableOrder.recipientEmail}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    recipientEmail: e.target.value,
                  })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>地址</Form.Label>
              <Form.Control
                type="text"
                value={editableOrder.address}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    address: e.target.value,
                  })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>運輸方式</Form.Label>
              <Form.Select
                value={editableOrder.transportationMethod}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    transportationMethod: e.target.value,
                  })
                }
              >
                <option value="delivery">宅配</option>
                <option value="seven">Seven 自取</option>
                <option value="family">Family 自取</option>
              </Form.Select>
            </Form.Group>

            {/* 優惠價功能 
            <Form.Group className="mb-3">
              <Form.Check
                type="checkbox"
                label="使用優惠價"
                checked={editableOrder.useDiscount}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    useDiscount: e.target.checked,
                  })
                }
              />
              {editableOrder.useDiscount && (
                <Form.Control
                  className="mt-2"
                  type="number"
                  value={editableOrder.discountPrice}
                  onChange={(e) =>
                    setEditableOrder({
                      ...editableOrder,
                      discountPrice: parseInt(e.target.value) || 0,
                    })
                  }
                />
              )}
            </Form.Group>
            */}

            <Form.Group className="mb-3">
              <Form.Label>備註</Form.Label>
              <Form.Control
                type="text"
                value={editableOrder.note}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    note: e.target.value,
                  })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>訂單狀態</Form.Label>
              <Form.Select
                value={editableOrder.status}
                onChange={(e) =>
                  setEditableOrder({
                    ...editableOrder,
                    status: e.target.value,
                  })
                }
              >
                <option value="待確認">待確認</option>
                <option value="待出貨">待出貨</option>
                <option value="已出貨">已出貨</option>
                <option value="已完成">已完成</option>
                <option value="已取消">已取消</option>
              </Form.Select>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowOrderModal(false)}>
            取消
          </Button>
          <Button
            variant="primary"
            onClick={updateOrder}
            style={{
              backgroundColor: "var(--accent-color)",
              borderColor: "var(--accent-color)",
            }}
          >
            儲存
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}
