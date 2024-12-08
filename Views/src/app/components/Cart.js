"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { useSelector, useDispatch } from "react-redux";
import { Container, Table, Button } from "react-bootstrap";
import { updateQuantity, removeFromCart } from "../redux/slices/cartSlice";
import config from "../config";
import axios from "axios";

const Cart = () => {
  const router = useRouter();
  const dispatch = useDispatch();
  const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品
  const { token } = useSelector((state) => state.user); // 獲取登入Token
  const [cartProduct, setCartProduct] = useState([]);
  let endpoint = config.apiBaseUrl;

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
      console.error("產品Mapping失敗：", err);
    }
  };


  useEffect(() => {
    if (cart.length > 0) {
      productAndCartMapping();
    }
  }, [cart]);

  // 更新購物車 API
  const updateCartAPI = async (cart_id, quantity) => {
    try {
      await axios.patch(
        `${endpoint}/frontstage/v1/cart/${cart_id}`,
        { quantity },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
    } catch (err) {
      console.error("更新購物車失敗：", err);
    }
  };

  // 操作購物車數量
  const handleIncrease = (pid, cart_id) => {
    dispatch(updateQuantity({ pid, quantity: 1 }));
    updateCartAPI(cart_id, 1);
  };

  const handleDecrease = (pid, cart_id) => {
    dispatch(updateQuantity({ pid, quantity: -1 }));
    updateCartAPI(cart_id, -1);
  };

  const handleRemove = (pid, cart_id) => {
    dispatch(removeFromCart(pid));
    try {
      axios.delete(`${endpoint}/frontstage/v1/cart/${cart_id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (err) {
      console.error("移除購物車失敗：", err);
    }
  };

  // 計算總額
  const calculateTotal = () => {
    return cartProduct.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  return (
    <Container className="my-4">
      <h2 className="mb-4">購物車</h2>
      {cart.length === 0 ? (
        <p>您的購物車目前是空的。</p>
      ) : (
        <>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>圖片</th>
                <th>商品名稱</th>
                <th>價格</th>
                <th>數量</th>
                <th>小計</th>
                <th>操作</th>
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
                  <td>
                    <Button
                      variant="outline-dark"
                      size="sm"
                      onClick={() => handleDecrease(item.pid, item.cart_id)}
                      disabled={item.quantity === 1}
                    >
                      -
                    </Button>
                    <span className="mx-2">{item.quantity}</span>
                    <Button
                      variant="outline-dark"
                      size="sm"
                      onClick={() => handleIncrease(item.pid, item.cart_id)}
                    >
                      +
                    </Button>
                  </td>
                  <td>NT. {item.price * item.quantity}</td>
                  <td>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleRemove(item.pid, item.cart_id)}
                    >
                      移除
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          <div className="text-end">
            <h4>總額：NT. {calculateTotal()}</h4>
            <Button
              variant="primary"
              onClick={() => router.push(`/order/buy`)}
              style={{
                backgroundColor: "var(--accent-color)",
                borderColor: "var(--accent-color)",
              }}
            >
              前往結帳
            </Button>
          </div>
        </>
      )}
    </Container>
  );
};

export default Cart;
