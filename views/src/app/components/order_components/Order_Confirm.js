"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { useSelector, useDispatch } from "react-redux";
import { Container, Row, Col, Table, Button, Form } from "react-bootstrap";
import axios from "axios";
import config from "@/app/config";
import crypto from "crypto";

import { showToast } from "@/app/redux/slices/toastSlice";

const OrderConfirm = () => {
    const router = useRouter();
    const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品
    const { userInfo, token } = useSelector((state) => state.user); // 獲取登入 Token
    const [cartProduct, setCartProduct] = useState([]);
    const [recipientName, setRecipientName] = useState(userInfo.username);
    const [recipientPhone, setRecipientPhone] = useState(userInfo.phone);
    const [recipientEmail, setRecipientEmail] = useState(userInfo.email);
    const [address, setAddress] = useState(userInfo.address);
    const [transportationMethod, setTransportationMethod] = useState("delivery");
    const [paymentMethod, setPaymentMethod] = useState("匯款"); // 付款方式
    const [orderNote, setOrderNote] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const endpoint = config.apiBaseUrl;

    const dispatch = useDispatch();

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
            handleError("請完整填寫所有必填欄位！");
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
                paymentMethod, // 付款方式
                orderNote: orderNote,
                order_details: orderDetails,
            };

            // 提交訂單
            const response = await axios.post(`${endpoint}/frontstage/v1/orders`, orderData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            console.log(response)
            const date = new Date(response.data.created_at);
            const formatedCreatedAt = `${date.getFullYear()}/${String(date.getMonth() + 1).padStart(2, "0")}/${String(date.getDate()).padStart(2, "0")} ` +
                `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}:${String(date.getSeconds()).padStart(2, "0")}`;

            if (paymentMethod === "匯款")
                createCashFlowOrder("ATM", response.data.oid, formatedCreatedAt, response.data.totalAmount)
            else if ((paymentMethod === "信用卡"))
                createCashFlowOrder("Credit", response.data.oid, formatedCreatedAt, response.data.totalAmount)
            //handleSuccess("訂單已提交成功！");
            //router.push("/order/history");
        } catch (error) {
            console.error("提交訂單失敗：", error);
            handleError("提交訂單失敗，請重試。");
        } finally {
            setIsSubmitting(false);
        }
    };

    // 生成 CheckMacValue 函數
    const createCheckMacValue = (
        MerchantID,
        MerchantTradeNo,
        MerchantTradeDate,
        TotalAmount,
        TradeDesc,
        ItemName,
        ReturnURL,
        ChoosePayment,
        ClientBackURL
    ) => {
        const hashKey = config.hashKey;
        const hashIv = config.hashIv;

        const toEncode = `HashKey=${hashKey}&MerchantID=${MerchantID}&MerchantTradeNo=${MerchantTradeNo}` +
            `&MerchantTradeDate=${MerchantTradeDate}&PaymentType=aio&TotalAmount=${TotalAmount}&TradeDesc=${TradeDesc}` +
            `&ItemName=${ItemName}&ReturnURL=${ReturnURL}&ChoosePayment=${ChoosePayment}&EncryptType=1` +
            `&ClientBackURL=${ClientBackURL}&HashIV=${hashIv}`;

        // 1. URL Encode 字串
        const urlEncodedString = encodeURIComponent(toEncode);

        // 2. 將字串轉為小寫
        const lowerCaseString = urlEncodedString.toLowerCase();

        // 3. 使用 SHA256 進行加密
        const hash = crypto.createHash("sha256");
        hash.update(lowerCaseString);
        const hashedValue = hash.digest("hex");

        // 4. 將加密結果轉為大寫
        const checkMacValue = hashedValue.toUpperCase();

        return checkMacValue;
    };

    // 呼叫金流服務
    const createCashFlowOrder = async (paymentMethods, orderId, orderDate, orderAmount) => {
        const MerchantID = config.merchantId; // 特店編號
        const MerchantTradeNo = orderId; // 特店訂單編號
        const MerchantTradeDate = orderDate; // yyyy/MM/dd HH:mm:ss
        const PaymentType = "aio";
        const TotalAmount = orderAmount; // 交易金額
        const TradeDesc = "善泰團隊聖物"; // 交易描述
        const ItemName = "善泰團隊聖物"; // 商品名稱
        const ReturnURL = `${endpoint}/frontstage/v1/cash_flow_order`; // 付款完成通知回傳網址
        const ChoosePayment = paymentMethods; // Credit 或 ATM
        const EncryptType = 1; // 固定為 1
        const ClientBackURL = location.host;
        // 生成 CheckMacValue
        const CheckMacValue = createCheckMacValue(
            MerchantID,
            MerchantTradeNo,
            MerchantTradeDate,
            TotalAmount,
            TradeDesc,
            ItemName,
            ReturnURL,
            ChoosePayment,
            ClientBackURL
        );
        const cashFlowEndpoint = config.cashFlowEndpoint
        // 表單數據
        const formData = {
            MerchantID,
            MerchantTradeNo,
            MerchantTradeDate,
            PaymentType,
            TotalAmount,
            TradeDesc,
            ItemName,
            ReturnURL,
            ChoosePayment,
            CheckMacValue,
            EncryptType,
            ClientBackURL,
        };
        // 發送 POST 請求
        axios.post(cashFlowEndpoint, formData, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });
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
                            value={recipientName || ""}
                            onChange={(e) => setRecipientName(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId="formRecipientPhone" className="mb-3">
                        <Form.Label>收件人電話</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="請輸入收件人電話"
                            value={recipientPhone || ""}
                            onChange={(e) => setRecipientPhone(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId="formRecipientEmail" className="mb-3">
                        <Form.Label>收件人 Email</Form.Label>
                        <Form.Control
                            type="email"
                            placeholder="請輸入收件人 Email"
                            value={recipientEmail || ""}
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
                            value={address || ""}
                            onChange={(e) => setAddress(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId="formPaymentMethod" className="mb-3">
                        <Form.Label>付款方式</Form.Label>
                        <Form.Select
                            value={paymentMethod}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                        >
                            <option value="匯款">匯款</option>
                            <option value="信用卡">信用卡</option>
                            <option value="貨到付款">貨到付款</option>
                        </Form.Select>
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
