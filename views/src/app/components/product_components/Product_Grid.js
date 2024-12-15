"use client";

import React from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { Container, Row, Col, Card, Button, Spinner } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "@/app/redux/slices/cartSlice";
import config from "@/app/config";
import axios from "axios";

import { showToast } from "@/app/redux/slices/toastSlice";

const Product_Grid = ({ initialProducts }) => {
  const router = useRouter();
  const dispatch = useDispatch();
  const endpoint = config.apiBaseUrl;
  const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品

  // 取得用戶資料
  const { userInfo, token } = useSelector((state) => state.user);

  if (!initialProducts) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載產品...</p>
      </Container>
    );
  } else if (initialProducts.length === 0) {
    return (
      <Container className="text-center my-4">
        <p className="mt-2">目前無產品上架</p>
      </Container>
    );
  }

  const handleAddCart = async (product) => {
    try {
      const productCheck = initialProducts.find((item) => item.pid === product.pid);
      const cartCheck = cart.find((item) => item.pid == product.pid);
      if (cartCheck.quantity >= productCheck.remain) {
        handleError(`超出庫存限制，剩餘數量僅有 ${product.remain}`);
        return;
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
      handleSuccess("加入成功！")
    } catch (error) {
      console.error("無法將商品加入購物車：", error);
      // 在這裡可以選擇設計錯誤處理，例如恢復 Redux 的購物車數據或顯示錯誤提示
    }
  };

  // 控制彈出視窗訊息區
  const handleSuccess = (message) => {
    dispatch(showToast({ message: message, variant: "success" }));
  };

  const handleError = (message) => {
    dispatch(showToast({ message: message, variant: "danger" }));
  };


  return (
    <Container className="my-4">
      <Row xs={2} md={3} xl={4} xxl={5}>
        {initialProducts.map((product) => (
          <Col xs={6} md={3} key={product.pid} className="mb-4">
            <Card className="text-center product-card">
              <Card.Img
                variant="top"
                src={product.productImageUrl}
                alt={product.title_cn}
                onClick={() => router.push(`/product/${product.pid}`)}
                style={{ cursor: "pointer" }} />
              <Card.Body>
                <Card.Title
                  onClick={() => router.push(`/product/${product.pid}`)}
                  style={{ cursor: "pointer" }}>
                  {product.title_cn}
                </Card.Title>
                <Card.Text>NT. {product.price}</Card.Text>
                <Button variant="outline-dark" size="sm">購買</Button>
                <Button variant="outline-dark" size="sm" onClick={() => handleAddCart(product)}>加入購物車</Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default Product_Grid;