"use client";  // 設定為客戶端組件

import React, { useState, useEffect } from 'react';
import { Navbar, Nav, Container, NavDropdown, Badge } from 'react-bootstrap';
import { useRouter } from 'next/navigation';
import LoginModal from './Login_Modal';
import { useDispatch, useSelector } from "react-redux";
import { logout } from '../redux/slices/userSlice';
import { setCartItems } from '../redux/slices/cartSlice';
import { FaShoppingCart } from "react-icons/fa";
import axios from "axios";
import config from '../config';


export default function NavigationBar() {
  const router = useRouter();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const dispatch = useDispatch();
  const endpoint = config.apiBaseUrl;

  // 從 Redux 中取出會員資訊和購物車資訊
  const { userInfo, isAuthenticated, token } = useSelector((state) => state.user);
  const cartItems = useSelector((state) => state.cart.items);

  // 計算購物車商品總數
  const cartCount = cartItems.reduce((total, item) => total + item.quantity, 0);

  // 獲取購物車資料
  const fetchCartItems = async () => {
    try {
      const response = await axios.get(`${endpoint}/frontstage/v1/user_cart/${userInfo.uid}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response.data);
      dispatch(setCartItems(response.data)); // 更新購物車商品數量到 Redux store
    } catch (error) {
      console.error("無法拉取購物車數據：", error);
    }
  };

  // 當組件加載時獲取購物車數量
  useEffect(() => {
    // 如果已經認證過，用戶登入則呼叫購物車數據
    if (isAuthenticated) {
      fetchCartItems()
    }
  }, [isAuthenticated, dispatch]);

  const handleNavLink = (path) => {
    router.push(path);
  };

  const handleLogout = () => {
    dispatch(logout());
    router.push("/");
  }

  // 控制彈出視窗顯示的函數
  const handleShowLoginModal = () => setShowLoginModal(true);
  const handleCloseLoginModal = () => setShowLoginModal(false);

  return (
    <>
      <Navbar className="navbar" expand="lg">
        <Container>
          <Navbar.Brand onClick={() => handleNavLink('/')}>善泰團隊</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mx-auto">
              <Nav.Link onClick={() => handleNavLink('/')}>首頁</Nav.Link>
              <Nav.Link onClick={() => handleNavLink('/faq')}>Q&A</Nav.Link>
              <Nav.Link onClick={() => handleNavLink('/contact')}>聯絡我們</Nav.Link>
            </Nav>

            <Nav className="align-items-center">
              {/* 購物車圖示 */}
              <Nav.Link onClick={() => handleNavLink('/product/cart')} className="position-relative">
                <FaShoppingCart size={24} />
                {cartCount > 0 && (
                  <Badge
                    pill
                    bg="danger"
                    className="position-absolute top-0 start-100 translate-middle badge rounded-circle"
                    style={{ fontSize: '0.75rem' }}
                  >
                    {cartCount}
                  </Badge>
                )}
              </Nav.Link>

              {isAuthenticated ? (
                // 已登入，顯示會員名稱和下拉選單
                <NavDropdown title={userInfo.username == "" ? "會員" : userInfo.username} id="user-dropdown">
                  <NavDropdown.Item onClick={() => handleNavLink("/orders")}>
                    訂單管理
                  </NavDropdown.Item>
                  <NavDropdown.Item onClick={() => handleNavLink("/profile")}>
                    會員資料
                  </NavDropdown.Item>
                  {userInfo.isAdmin && (
                    <NavDropdown.Item onClick={() => handleNavLink("/backstage/product_management")}>
                      後台管理
                    </NavDropdown.Item>
                  )}
                  <NavDropdown.Divider />
                  <NavDropdown.Item onClick={handleLogout}>
                    登出
                  </NavDropdown.Item>
                </NavDropdown>
              ) : (
                // 未登入，顯示登入按鈕
                <Nav.Link onClick={handleShowLoginModal}>
                  <i
                    className="bi bi-person-circle"
                    style={{ fontSize: "1.5rem" }}
                  ></i>
                </Nav.Link>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {/* Login_Modal 彈出視窗 */}
      <LoginModal show={showLoginModal} handleClose={handleCloseLoginModal} />
    </>
  );
}
