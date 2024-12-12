"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { useSelector } from "react-redux";
import { Container, Row, Col, Table, Button, Form } from "react-bootstrap";
import axios from "axios";
import config from "@/app/config";

const OrderConfirm = () => {
    const router = useRouter();
    const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品
    const { userInfo, token } = useSelector((state) => state.user); // 獲取登入 Token
    const [cartProduct, setCartProduct] = useState([]);
    const [address, setAddress] = useState("");
    const [recipientName, setRecipientName] = useState("");
    const [recipientPhone, setRecipientPhone] = useState("");
    const [recipientEmail, setRecipientEmail] = useState("");
    const [transportationMethod, setTransportationMethod] = useState("delivery");
    const [orderNote, setOrderNote] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const endpoint = config.apiBaseUrl;

    // 同步購物車與商品詳細資料
    const productAndCartMapping = async () => {
        try {
            const productPromises = cart.map(async (item) => {
                const response = await axios.get(`${endpoint}/frontstage/v1/product_by_pid/${item.pid}`);
                return {
                    ...item,
                    ...response.data,
                };
            });

            const resolvedProducts = await Promise.all(productPromises);
            setCartProduct(resolvedProducts);
        } catch (err) {
            console.error("產品 Mapping 失敗：", err);
        }
    };

    useEffect(() => {
        if (cart.length > 0) {
            productAndCartMapping();
        }
    }, [cart]);

    // 計算總額
    const calculateTotal = () => {
        return cartProduct.reduce((total, item) => total + item.price * item.quantity, 0);
    };

    // 提交訂單
    const handleSubmitOrder = async () => {
        if (!recipientName || !recipientPhone || !recipientEmail || !address) {
            alert("請完整填寫所有必填欄位！");
            return;
        }

        setIsSubmitting(true);

        try {
            const orderDetails = cartProduct.map((item) => ({
                pid: item.pid,
                productNumber: item.quantity,
                price: item.price,
                subtotal: item.quantity * item.price,
            }));

            const totalAmount = orderDetails.reduce((sum, item) => sum + item.subtotal, 0);

            // 組合訂單資料
            const orderData = {
                uid: userInfo.uid,
                totalAmount: totalAmount,
                address: address,
                recipientName: recipientName,
                recipientPhone: recipientPhone,
                recipientEmail: recipientEmail,
                transportationMethod,
                orderNote: orderNote,
                order_details: orderDetails,
            };

            // 提交訂單
            await axios.post(`${endpoint}/frontstage/v1/orders`, orderData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            alert("訂單已提交成功！");
            router.push("/order/history");
        } catch (error) {
            console.error("提交訂單失敗：", error);
            alert("提交訂單失敗，請重試。");
        } finally {
            setIsSubmitting(false);
        }
    };


    return (
        <Container className="my-4">
            <h2 className="mb-4">確認訂單</h2>

            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>圖片</th>
                        <th>商品名稱</th>
                        <th>價格</th>
                        <th>數量</th>
                        <th>小計</th>
                    </tr>
                </thead>
                <tbody>
                    {cartProduct.map((item) => (
                        <tr key={item.pid}>
                            <td>
                                <img
                                    src={item.productImageUrl}
                                    alt={item.title_cn}
                                    width="100"
                                    height="100"
                                />
                            </td>
                            <td>{item.title_cn}</td>
                            <td>NT. {item.price}</td>
                            <td>{item.quantity}</td>
                            <td>NT. {item.price * item.quantity}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Row className="mt-4">
                <Col xs={12} md={6}>
                    <Form.Group controlId="formRecipientName" className="mb-3">
                        <Form.Label>收件人姓名</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="請輸入收件人姓名"
                            value={recipientName}
                            onChange={(e) => setRecipientName(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId="formRecipientPhone" className="mb-3">
                        <Form.Label>收件人電話</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="請輸入收件人電話"
                            value={recipientPhone}
                            onChange={(e) => setRecipientPhone(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId="formRecipientEmail" className="mb-3">
                        <Form.Label>收件人 Email</Form.Label>
                        <Form.Control
                            type="email"
                            placeholder="請輸入收件人 Email"
                            value={recipientEmail}
                            onChange={(e) => setRecipientEmail(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId="formTransportationMethod" className="mb-3">
                        <Form.Label>寄送方式</Form.Label>
                        <Form.Select
                            value={transportationMethod}
                            onChange={(e) => setTransportationMethod(e.target.value)}
                        >
                            <option value="delivery">宅配</option>
                            <option value="seven">Seven 自取</option>
                            <option value="family">Family 自取</option>
                        </Form.Select>
                    </Form.Group>

                    <Form.Group controlId="formAddress" className="mb-3">
                        <Form.Label>{transportationMethod === "delivery" ? "送貨地址" : "超商門市"}</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder={`請輸入${transportationMethod === "delivery" ? "送貨地址" : "超商門市名稱"}`}
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId="formNote" className="mb-3">
                        <Form.Label>訂單備註</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            placeholder="請輸入訂單備註（選填）"
                            value={orderNote}
                            onChange={(e) => setOrderNote(e.target.value)}
                        />
                    </Form.Group>
                </Col>

                <Col xs={12} md={6}>
                    <h4>訂單金額總計：NT. {calculateTotal()}</h4>
                    <Button
                        variant="primary"
                        className="mt-4"
                        onClick={handleSubmitOrder}
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? "提交中..." : "確認購買"}
                    </Button>
                </Col>
            </Row>
        </Container>
    );
};

export default OrderConfirm;
