"use client";

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useRouter } from 'next/navigation';
import { AiOutlineMail } from "react-icons/ai"; // 引入 react-icons 的 Email icon
import Image from "next/image";

export default function Footer() {
  const router = useRouter();

  const handleNavLink = (path) => {
    router.push(path);
  };
  return (
    <Container fluid className="footer mt-4 py-4">
      <Row className="justify-content-center text-center">
        <Col xs={12} sm={6} md={4}><a onClick={() => handleNavLink('/about')}>關於善泰團隊</a></Col>
        <Col xs={12} sm={6} md={4}>
          <h5>聯絡我們</h5>
          {/*
            <a onClick={() => handleNavLink("/member-services")}>
            <Image
              src="/line_icon.svg" // 確保圖片位於 public 資料夾內
              alt="Line Icon"
              width={20}
              height={20}
              className="me-2"
            />
            加入 Line 群
          </a>
          <br />
          */}
          <a>
            <AiOutlineMail style={{ marginRight: "5px" }} />
            Email
          </a>
        </Col>
        <Col xs={12} sm={6} md={4}>
          <h5>條例條款</h5>
          <a onClick={() => handleNavLink('shanthaiteam@gmail.com')}>使用者條款</a>
        </Col>
      </Row>
      <Row className="justify-content-center text-center mt-3">
        <Col xs="auto">
          <a
            href="https://www.facebook.com/people/%E5%96%84%E6%B3%B0%E5%9C%98%E9%9A%8A-%E6%B3%B0%E5%9C%8B%E5%8D%97%E5%82%B3%E8%81%96%E7%89%A9%E8%AB%8B%E4%BE%9B/61553678884399/"
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontSize: "1.5rem", cursor: "pointer" }}
          >
            <i className="bi bi-facebook"></i>
          </a>
        </Col>
        <Col xs="auto">
          <a
            href="https://www.instagram.com/shanthaiteam/"
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontSize: "1.5rem", cursor: "pointer" }}
          >
            <i className="bi bi-instagram"></i>
          </a>
        </Col>
        <Col xs="auto">
          <a
            href="https://x.com/ShanThai666"
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontSize: "1.5rem", cursor: "pointer" }}
          >
            <i className="bi bi-twitter"></i>
          </a>
        </Col>
        <Col xs="auto">
          <a
            href="https://www.threads.net/@shanthaiteam"
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontSize: "1.5rem", cursor: "pointer" }}
          >
            <i className="bi bi-threads-fill"></i>
          </a>
        </Col>
      </Row>
    </Container>
  );
}
