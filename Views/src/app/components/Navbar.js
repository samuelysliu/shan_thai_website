"use client";  // 設定為客戶端組件

import React from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

export default function NavigationBar() {
  const router = useRouter();

  const handleNavLink = (path) => {
    router.push(path);
  };

  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand onClick={() => handleNavLink('/')}>My Website</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link onClick={() => handleNavLink('/')}>Home</Nav.Link>
            <Nav.Link onClick={() => handleNavLink('/about')}>About</Nav.Link>
            <Nav.Link onClick={() => handleNavLink('/contact')}>Contact</Nav.Link>
            <Nav.Link onClick={() => handleNavLink('/login')}>Login</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
