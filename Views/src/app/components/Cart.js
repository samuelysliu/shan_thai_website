"use client";

import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Container, Row, Col, Table, Button } from "react-bootstrap";
import { updateQuantity, removeFromCart } from "../redux/slices/cartSlice";

const Cart = () => {
  const dispatch = useDispatch();
  const cart = useSelector((state) => state.cart.items); // 從 Redux 獲取購物車商品

  // 計算總額
  const calculateTotal = () => {
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  const handleIncrease = (pid) => {
    dispatch(updateQuantity({ pid, quantity: 1 })); // 增加數量
  };

  const handleDecrease = (pid) => {
    dispatch(updateQuantity({ pid, quantity: -1 })); // 減少數量
  };

  const handleRemove = (pid) => {
    dispatch(removeFromCart(pid)); // 移除商品
  };

  const handleCheckout = () => {
    // 導航到結帳頁面
    console.log("前往結帳");
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
              {cart.map((item) => (
                <tr key={item.pid}>
                  <td>
                    <img
                      src={item.productImageUrl}
                      alt={item.title_cn}
                      width="80"
                      height="80"
                    />
                  </td>
                  <td>{item.title_cn}</td>
                  <td>NT. {item.price}</td>
                  <td>
                    <Button
                      variant="outline-dark"
                      size="sm"
                      onClick={() => handleDecrease(item.pid)}
                      disabled={item.quantity === 1}
                    >
                      -
                    </Button>
                    <span className="mx-2">{item.quantity}</span>
                    <Button
                      variant="outline-dark"
                      size="sm"
                      onClick={() => handleIncrease(item.pid)}
                    >
                      +
                    </Button>
                  </td>
                  <td>NT. {item.price * item.quantity}</td>
                  <td>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleRemove(item.pid)}
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
              onClick={handleCheckout}
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
