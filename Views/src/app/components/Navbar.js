"use client";  // 設定為客戶端組件

import React, { useState } from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { useRouter } from 'next/navigation';
import LoginModal from './Login_Modal';
import { useSelector } from 'react-redux';
import { useDispatch } from "react-redux";
import { logout } from '../redux/slices/userSlice';

export default function NavigationBar() {
  const router = useRouter();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const dispatch = useDispatch();

  // 從 Redux 中取出會員資訊
  const { userInfo, isAuthenticated } = useSelector((state) => state.user);

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
              <Nav.Link onClick={() => handleNavLink('/qna')}>Q&A</Nav.Link>
              <Nav.Link onClick={() => handleNavLink('/contact')}>聯絡我們</Nav.Link>
            </Nav>
            <Nav>
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
