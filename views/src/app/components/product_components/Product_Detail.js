"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "@/app/redux/slices/cartSlice";
import { Container, Row, Col, Image, Button, Card, Spinner } from "react-bootstrap";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示
import axios from "axios";
import config from "@/app/config";

import { showToast } from "@/app/redux/slices/toastSlice";

const Product_Detail = ({ pid }) => {
  const router = useRouter();
  const endpoint = config.apiBaseUrl;
  // 取得用戶資料
  const { userInfo, token } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品

  // 立即購買的邏輯
  const handleBuyNow = async (product) => {
    if (await handleAddCart(product)) {
      router.push(`/order/buy`)
      return;
    }
  };

  // 加入購物車的邏輯
  const handleAddCart = async (product) => {
    if (userInfo === null) {
      handleSuccess("請先登入會員");
      return false;
    }

    try {
      const cartCheck = cart.find((item) => item.pid == product.pid);
      let checkNum = 0;

      if (cartCheck != undefined) { // 代表購物車有此項目
        checkNum = cartCheck.quantity;
      }

      if (checkNum >= product.remain) {
        handleError(`超出庫存限制，剩餘數量僅有 ${product.remain}`)
        return false;
      }

      let cartObject = {
        uid: userInfo.uid,
        pid: product.pid,
        quantity: 1,
      }

      // 然後呼叫後端 API，將該商品加入購物車
      await axios.post(`${endpoint}/frontstage/v1/cart`, cartObject,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

      // 更新 Redux 中的購物車
      dispatch(addToCart(cartObject));
      handleSuccess("加入成功！");
      return true;
    } catch (error) {
      console.error("無法將商品加入購物車：", error);
      return false;
    }
  };

  const [loading, setLoading] = useState(true);
  const [product, setProduct] = useState(
    {
      "pid": 0,
      "productImageUrl": "",
      "title_cn": "",
      "price": 0,
      "remain": 0,
      "content_cn": 0
    }
  );

  // 取得產品詳情 API
  const fetchProductDetail = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${endpoint}/frontstage/v1/product_by_pid/${pid}`,
        {
          headers: {
            Authorization: `Bearer ${token}`, // 加入 Authorization header
          },
        }
      );
      setProduct(response.data); // 更新訂單列表
    } catch (err) {
      handleError("無法加載訂單資料，請稍後再試。");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProductDetail();
  }, [pid])

  if (loading) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品詳情...</p>
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
      <Col xs={12}>
        <Button variant="link" onClick={() => router.back()}>
          <FaArrowLeft /> 返回
        </Button>
      </Col>
      <Row className="align-items-start">
        <Col xs={12} md={6} className="text-center">
          <Image src={product.productImageUrl} alt={product.title_cn} fluid rounded />
        </Col>
        <Col xs={12} md={6}>
          <Card className="border-0">
            <Card.Body>
              <Card.Title className="product-title" as="h1">{product.title_cn}</Card.Title>
              <Card.Text className="product-price text-muted">
                <span style={{ fontSize: '1.75rem' }}>NT. {product.price}</span>
              </Card.Text>
              <Card.Text className="product-stock">
                <span>庫存數量：{product.remain}</span>
              </Card.Text>
              {/* 按鈕區域 */}
              <div className="d-grid gap-2 mt-4">
                <Button
                  variant="outline-primary"
                  size="lg"
                  onClick={() => handleAddCart(product)}
                  disabled={product.remain <= 0}
                >
                  加入購物車
                </Button>
                <Button
                  variant="primary"
                  size="lg"
                  onClick={() => handleBuyNow(product)}
                  disabled={product.remain <= 0}
                >
                  直接購買
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      {/* 底部：產品詳細說明 */}
      <Row className="mt-5">
        <Col>
          <h3>產品說明</h3>
          <div dangerouslySetInnerHTML={{ __html: product.content_cn }}></div>
        </Col>
      </Row>
    </Container>
  );
}

export default Product_Detail;