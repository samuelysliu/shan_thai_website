"use client";

import React from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "@/app/redux/slices/cartSlice";
import { Container, Row, Col, Image, Button, Card } from "react-bootstrap";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示
import axios from "axios";
import config from "@/app/config";

const Product_Detail = ({ product }) => {
  const router = useRouter();
  let endpoint = config.apiBaseUrl;
  // 取得用戶資料
  const { userInfo, token } = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const handleBuyNow = () => {
    // 立即購買的邏輯
    console.log("立即購買", product.pid);
  };

  const handleAddCart = async (product) => {
    console.log(product)
    try {
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

  return (
    <Container className="my-4">
      <Button variant="link" onClick={() => router.back()} className="mb-3">
        <FaArrowLeft />返回
      </Button>
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