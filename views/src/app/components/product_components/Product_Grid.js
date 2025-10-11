// app/components/product_components/Product_Grid.js
"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { Container, Row, Col, Card, Button, Spinner, Carousel } from "react-bootstrap";
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
  const [productImages, setProductImages] = useState({});
  const observerRef = useRef(null);
  const loadedPids = useRef(new Set()); // 紀錄已載入的 pid

  // 取得用戶資料
  const { userInfo, token } = useSelector((state) => state.user);

  // 取得圖片資訊 (Lazy Load)
  const loadImages = async (pid) => {
    if (loadedPids.current.has(pid)) return; // 防止重複請求
    
    try {
      const response = await axios.get(`${endpoint}/frontstage/v1/product_images/${pid}`);
      setProductImages((prev) => ({ ...prev, [pid]: response.data.productImages || [] }));
      loadedPids.current.add(pid); // 確保已載入
    } catch (error) {
      console.error("無法獲取圖片:", error);
      setProductImages((prev) => ({ ...prev, [pid]: [] })); // 失敗時，設為空陣列避免錯誤
      loadedPids.current.add(pid); // 避免反覆請求
    }
  };

  // 觀察畫面中的產品，當它進入視野時請求圖片
  const handleIntersection = (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const pid = entry.target.dataset.pid;
        loadImages(pid);
        observer.unobserve(entry.target); // 避免重複觀察，提高效能
      }
    });
  };

  useEffect(() => {
    if (!observerRef.current) {
      const observer = new IntersectionObserver(handleIntersection, { rootMargin: "100px" });
      observerRef.current = observer;
    }

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect(); // 確保在卸載時清除 observer
      }
    };
  }, []);

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
      const productCheck = initialProducts.find((item) => item.pid === product.pid);
      const cartCheck = cart.find((item) => item.pid == product.pid);
      let checkNum = 0;
      if (cartCheck != undefined) { // 代表購物車有此項目
        checkNum = cartCheck.quantity;
      }

      if (checkNum >= productCheck.remain) {
        handleError(`超出庫存限制，剩餘數量僅有 ${product.remain}`);
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

      // GA 紀錄
      if (typeof window !== 'undefined' && window.gtag) {
        window.gtag('event', 'add_to_cart', {
          currency: 'TWD',
          value: product.price,
          items: [
            {
              item_id: product.pid,
              item_name: product.title_cn,
              price: product.price,
              quantity: 1,
              user_id: userInfo.uid
            },
          ],
        });
      }
      
      return true;
    } catch (error) {
      console.error("無法將商品加入購物車：", error);
      return false;
    }
  };

  // 控制彈出視窗訊息區
  const handleSuccess = (message) => {
    dispatch(showToast({ message: message, variant: "success" }));
  };

  const handleError = (message) => {
    dispatch(showToast({ message: message, variant: "danger" }));
  };

  // 沒有產品的處理顯示
  if (!initialProducts || initialProducts[0] === 0) {
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


  return (
    <Container className="my-4">
      <Row xs={2} md={3} xl={4} xxl={5}>
        {initialProducts.map((product) => (
          <Col xs={6} md={3} key={product.pid} className="mb-4">

            <Card
              className="text-center product-card"
              data-pid={product.pid}
              ref={(el) => {
                if (el && observerRef.current) {
                  observerRef.current.observe(el);
                }
              }}
            >
              {/* 圖片輪播區塊 */}
              <div style={{ cursor: "pointer" }}>
                {productImages[product.pid] && productImages[product.pid].length > 0 ? (
                  <Carousel interval={3000} fade>
                    {productImages[product.pid].map((img, index) => (
                      <Carousel.Item key={index}>
                        <Card.Img
                          variant="top"
                          src={img}
                          alt={product.title_cn}
                          style={{ height: "200px", objectFit: "cover" }}
                          onClick={() => router.push(`/product/${product.pid}`)}
                          loading="lazy"
                        />
                      </Carousel.Item>
                    ))}
                  </Carousel>
                ) : (
                  <Card.Img
                    variant="top"
                    src="loading-placeholder.png"
                    alt={product.title_cn}
                    style={{ height: "200px" }}
                    onClick={() => router.push(`/product/${product.pid}`)}
                    loading="lazy"
                  />
                )}
              </div>

              <Card.Body>
                <Card.Title
                  onClick={() => router.push(`/product/${product.pid}`)}
                  style={{ cursor: "pointer" }}>
                  {product.title_cn}
                </Card.Title>
                <Card.Text>NT. {product.price}</Card.Text>
                <Button variant="outline-dark" size="sm" onClick={() => handleBuyNow(product)}>購買</Button>
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