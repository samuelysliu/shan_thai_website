"use client";  // 設定為客戶端組件

import React, { useState } from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { useRouter } from 'next/navigation';
import LoginModal from './Login_Modal';

export default function NavigationBar() {
  const router = useRouter();
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleNavLink = (path) => {
    router.push(path);
  };

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
              <Nav.Link onClick={handleShowLoginModal}>
                <i className="bi bi-person-circle" style={{ fontSize: '1.5rem' }}></i>
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {/* Login_Modal 彈出視窗 */}
      <LoginModal show={showLoginModal} handleClose={handleCloseLoginModal} />
    </>
  );
}
