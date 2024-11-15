"use client";

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

export default function Footer() {
  const router = useRouter();

  const handleNavLink = (path) => {
    router.push(path);
  };
  return (
    <Container fluid className="footer mt-4 py-4">
      <Row className="justify-content-center text-center">
        <Col xs={12} sm={6} md={3}><a onClick={() => handleNavLink('/about')}>關於善泰團隊</a></Col>
        <Col xs={12} sm={6} md={3}><a onClick={() => handleNavLink('/purchase-info')}>購物須知</a></Col>
        <Col xs={12} sm={6} md={3}><a onClick={() => handleNavLink('/member-services')}>會員服務</a></Col>
        <Col xs={12} sm={6} md={3}><a onClick={() => handleNavLink('/terms')}>條例條款</a></Col>
      </Row>
      <Row className="justify-content-center text-center mt-3">
        <Col xs="auto"><i className="bi bi-facebook" style={{ fontSize: '1.5rem', cursor: 'pointer' }} onClick={() => router.push('https://www.facebook.com')}></i></Col>
        <Col xs="auto"><i className="bi bi-instagram" style={{ fontSize: '1.5rem', cursor: 'pointer' }} onClick={() => router.push('https://www.instagram.com')}></i></Col>
        <Col xs="auto"><i className="bi bi-twitter" style={{ fontSize: '1.5rem', cursor: 'pointer' }} onClick={() => router.push('https://www.twitter.com')}></i></Col>
      </Row>
    </Container>
  );
}
