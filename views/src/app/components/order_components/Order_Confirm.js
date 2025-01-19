"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { useSelector, useDispatch } from "react-redux";
import { Container, Row, Col, Table, Button, Form } from "react-bootstrap";
import axios from "axios";
import config from "@/app/config";
import { generateRandomString, createCheckMacValue, userDevice } from "../Tools"

import { showToast } from "@/app/redux/slices/toastSlice";

const OrderConfirm = () => {
    const router = useRouter();
    const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品
    const { userInfo, token } = useSelector((state) => state.user); // 獲取登入 Token

    const [cartProduct, setCartProduct] = useState([]);
    const [recipientName, setRecipientName] = useState(userInfo?.username || "");
    const [recipientPhone, setRecipientPhone] = useState(userInfo?.phone || "");
    const [recipientEmail, setRecipientEmail] = useState(userInfo?.email || "");
    const [zipCode, setZipCode] = useState("");
    const [address, setAddress] = useState(userInfo?.address || "");
    const [storeId, setStoreId] = useState("");
    const [shanThaiToken, setShanThaiToken] = useState(0)
    const [useShanThaiToken, setUseShanThaiToken] = useState(0)
    const [transportationMethod, setTransportationMethod] = useState("delivery");
    const [paymentMethod, setPaymentMethod] = useState("匯款"); // 付款方式
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

    // 同步善泰幣數量
    const getShanThaiTokenBalance = async () => {
        try {
            const response = await axios.get(`${endpoint}/frontstage/v1/tokens/${userInfo.uid}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setShanThaiToken(response.data.balance);
        } catch (err) {
            console.error("取得善泰幣資訊失敗：", err);
        }
    }

    useEffect(() => {
        if (cart.length > 0) {
            productAndCartMapping();
        }
        getShanThaiTokenBalance();
    }, [cart, userInfo]);

    // 計算總額
    const calculateTotal = () => {
        return cartProduct.reduce((total, item) => total + item.price * item.quantity, 0) - useShanThaiToken;
    };

    // 提交訂單
    const handleSubmitOrder = async () => {
        if (!recipientName || !recipientPhone || !recipientEmail
            || !address || address === "等待選擇中...") {
            handleError("請完整填寫所有必填欄位！");
            return;
        } else if (transportationMethod === "delivery" && address.length <= 6) {
            handleError("請填寫正確的地址欄位！");
            return;
        } else if (transportationMethod === "delivery") {
            setIsSubmitting(true);
            const response = await axios.get(`${endpoint}/frontstage/v1/address_exist/${address}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.data.success) {
                handleError("請填寫正確的地址欄位！");
                setIsSubmitting(false);
                return;
            }
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

            let postAddress = ""
            if (transportationMethod === "delivery")
                postAddress = address
            else postAddress = storeId


            // 組合訂單資料
            const orderData = {
                uid: userInfo.uid,
                totalAmount: totalAmount,
                zipCode: zipCode,
                address: postAddress,
                recipientName: recipientName,
                recipientPhone: recipientPhone,
                recipientEmail: recipientEmail,
                transportationMethod: transportationMethod,
                paymentMethod: paymentMethod, // 付款方式
                shanThaiToken: useShanThaiToken,
                orderNote: "",
                order_details: orderDetails,
            };

            // 提交訂單
            const response = await axios.post(`${endpoint}/frontstage/v1/orders`, orderData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const date = new Date(response.data.created_at);
            const formatedCreatedAt = `${date.getFullYear()}/${String(date.getMonth() + 1).padStart(2, "0")}/${String(date.getDate()).padStart(2, "0")} ` +
                `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}:${String(date.getSeconds()).padStart(2, "0")}`;

            let orderAmount = response.data.totalAmount;

            if (response.data.useDiscount) {
                orderAmount = response.data.discountPrice;
            }

            if (paymentMethod === "匯款")
                createCashFlowOrder("ATM", response.data.oid, formatedCreatedAt, orderAmount)
            else if ((paymentMethod === "信用卡"))
                createCashFlowOrder("Credit", response.data.oid, formatedCreatedAt, orderAmount)


            handleSuccess("訂單已提交成功，正在確認付款資訊！");
            router.push("/order/history");
        } catch (error) {
            console.error("提交訂單失敗：", error);
            handleError("提交訂單失敗，請重試。");
        } finally {
            setIsSubmitting(false);
        }
    };

    // 呼叫金流服務
    const createCashFlowOrder = async (paymentMethods, orderId, orderDate, orderAmount) => {
        const params = {
            MerchantID: config.merchantId, // 特店編號
            MerchantTradeNo: orderId, // 特店交易編號
            MerchantTradeDate: orderDate, // yyyy/MM/dd HH:mm:ss
            PaymentType: "aio",
            TotalAmount: orderAmount, // 交易金額
            TradeDesc: "善泰團隊聖物", // 交易描述
            ItemName: "善泰團隊聖物", // 商品名稱
            ReturnURL: `${endpoint}/frontstage/v1/cash_flow_order`, // 回調地址
            ChoosePayment: paymentMethods, // Credit 或 ATM
            EncryptType: 1, // 固定為 1
            ClientBackURL: `${window.location.origin}/order/close`
        };

        // 生成 CheckMacValue
        const CheckMacValue = createCheckMacValue(params);

        // 添加 CheckMacValue 到表單數據
        params.CheckMacValue = CheckMacValue;

        const cashFlowEndpoint = config.cashFlowEndpoint

        const popupWindow = window.open("", "cashFlowWindow", "width=1200,height=600,scrollbars=no,resizable=no");
        // 建立隱藏的表單
        const form = document.createElement("form");
        form.method = "POST";
        form.action = cashFlowEndpoint;
        form.target = "cashFlowWindow"; // 在新分頁開啟

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

    // 取得超商地圖
    const getStoreMap = (logisticsSubType) => {
        const randomString = generateRandomString();

        const params = {
            MerchantID: config.merchantId, // 特店編號
            MerchantTradeNo: randomString, // 特店交易編號
            LogisticsType: "CVS", // 物流類型
            LogisticsSubType: logisticsSubType, // 物流子類型，FAMIC2C：全家店到店；UNIMARTC2C：7-ELEVEN超商交貨便；HILIFEC2C：萊爾富店到店；OKMARTC2C：OK超商店到店
            IsCollection: paymentMethod === "貨到付款" ? "Y" : "N", // 是否代收貨款，N：不代收貨款; Y：代收貨款
            ServerReplyURL: `${endpoint}/frontstage/v1/store_callback`,
            Device: userDevice === "mobile" ? 1 : 0
        };

        const storeMapEndpoint = config.storeMapEndpoint;

        const popupWindow = window.open("", "storeMapWindow", "width=800,height=600,scrollbars=no,resizable=no");
        // 建立隱藏的表單
        const form = document.createElement("form");
        form.method = "POST";
        form.action = storeMapEndpoint;
        form.target = "storeMapWindow";
        //form.target = "hiddenIframe";

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

        setAddress("等待選擇中...");
        // 定期檢查分頁是否被關閉
        const checkWindowClosed = setInterval(() => {
            if (popupWindow.closed) {
                clearInterval(checkWindowClosed); // 停止檢查
                console.log("分頁已關閉，開始獲取門市資訊...");
                getStoreData(randomString); // 呼叫後端 API
            }
        }, 5000);

    }

    // 處理寄送方式的邏輯
    const transportationLogic = (transport) => {
        setTransportationMethod(transport);
        if (transport === "seven")
            getStoreMap("UNIMARTC2C")
        else if (transport === "family")
            getStoreMap("FAMIC2C")
        else setAddress("");
    }

    // 跟後端要使用者選擇的超商資訊
    const getStoreData = async (tradeNo) => {
        try {
            const response = await axios.get(`${endpoint}/frontstage/v1/store_selection/${tradeNo}`);
            setAddress(response.data.cvs_store_name);
            setStoreId(response.data.cvs_store_id)
        } catch (err) {
            console.error(err);
        }
    }

    // 處理善泰幣的輸入
    const checkShanThaiToken = (e) => {
        const value = parseInt(e.target.value, 10); // 將輸入值轉為整數
        if (value >= 0 && value <= shanThaiToken && value < cartProduct.reduce((total, item) => total + item.price * item.quantity, 0) - 9) {
            setUseShanThaiToken(value);
        } else if (!value) {
            setUseShanThaiToken(0);
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
                            onChange={(e) => transportationLogic(e.target.value)}
                        >
                            <option value="delivery">宅配(中華郵政)</option>
                            <option value="seven">Seven 自取</option>
                            <option value="family">Family 自取</option>
                        </Form.Select>
                    </Form.Group>

                    {transportationMethod === "delivery" ?
                        <Form.Group controlId="formZipCode" className="mb-3">
                            <Form.Label>郵遞區號</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="請輸入郵遞區號3碼"
                                value={zipCode}
                                onChange={(e) => setZipCode(e.target.value)}
                                disabled={transportationMethod !== "delivery"}
                            />
                        </Form.Group>
                        : ""}

                    <Form.Group controlId="formAddress" className="mb-3">
                        <Form.Label>{transportationMethod === "delivery" ? "送貨地址" : "超商門市"}</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="請輸入完整送貨地址"
                            value={address || ""}
                            onChange={(e) => setAddress(e.target.value)}
                            disabled={transportationMethod !== "delivery"}
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
                            {
                                (transportationMethod !== "delivery" && calculateTotal() <= 20000)
                                    ? <option value="貨到付款">貨到付款</option>
                                    : ""
                            }
                        </Form.Select>
                    </Form.Group>
                </Col>

                <Col xs={12} md={6}>
                    <Row className="border-bottom mb-3">
                        <Form.Group controlId="token" className="mb-3">
                            <Form.Label>善泰幣(最多折抵至10元)</Form.Label>
                            <Form.Control
                                type="number"
                                placeholder="請輸入要使用的善泰幣數量"
                                value={useShanThaiToken || 0}
                                onChange={(e) => checkShanThaiToken(e)}
                            />
                        </Form.Group>
                        <p>剩餘數量：{shanThaiToken || 0}</p>
                    </Row>

                    <Row>
                        <h4>訂單金額總計：NT. {calculateTotal()}</h4>
                        <Button
                            variant="primary"
                            className="mt-4"
                            onClick={handleSubmitOrder}
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? "提交中..." : "確認購買"}
                        </Button>
                        <p>提醒您，因應物流公司規定，選擇宅配或是總金額超過兩萬塊，無法貨到付款，造成您的不便，敬請見諒！</p>
                    </Row>
                </Col>
            </Row>

        </Container>
    );
};

export default OrderConfirm;
