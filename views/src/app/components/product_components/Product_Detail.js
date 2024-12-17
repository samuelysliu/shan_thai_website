"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "@/app/redux/slices/cartSlice";
import { Container, Row, Col, Image, Button, Card } from "react-bootstrap";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示
import axios from "axios";
import config from "@/app/config";

import { showToast } from "@/app/redux/slices/toastSlice";

const Product_Detail = ({ product }) => {
  const router = useRouter();
  const endpoint = config.apiBaseUrl;
  // 取得用戶資料
  const { userInfo, token } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品


  const handleBuyNow = () => {
    // 立即購買的邏輯
    console.log("立即購買", product.pid);
  };

  const handleAddCart = async (product) => {
    try {
      const cartCheck = cart.find((item) => item.pid == product.pid);
      const checkNum = 0;

      if (cartCheck != undefined) { // 代表購物車有此項目
        checkNum = cartCheck.quantity;
      }

      if (checkNum >= product.remain) {
        handleError(`超出庫存限制，剩餘數量僅有 ${product.remain}`)
        return;
      }

      let cartObject = {
        uid: userInfo.uid,
        pid: product.pid,
        quantity: 1,
      }
      console.log(cartObject)

      // 然後呼叫後端 API，將該商品加入購物車
      await axios.post(`${endpoint}/frontstage/v1/cart`, cartObject,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

      // 更新 Redux 中的購物車
      dispatch(addToCart(cartObject));
      handleSuccess("加入成功！")
    } catch (error) {
      console.error("無法將商品加入購物車：", error);
      // 在這裡可以選擇設計錯誤處理，例如恢復 Redux 的購物車數據或顯示錯誤提示
    }
  };

  if (!product) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品...</p>
      </Container>
    );
  } else if (product.length === 0) {
    return (
      <Container className="text-center my-4">
        <p className="mt-2">查無此產品</p>
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
          <p>{product.content_cn}</p>
        </Col>
      </Row>
    </Container>
  );
}

export default Product_Detail;