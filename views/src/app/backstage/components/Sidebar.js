// src/app/components/Sidebar.js
"use client";

import React from 'react';
import { Col, Button } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

export default function Sidebar() {
  const router = useRouter();

  const handleNavigation = (path) => {
    router.push(path);
  };

  return (
    <Col xs={2} className="sidebar" style={{ backgroundColor: "var(--primary-color)", color: "var(--light-text-color)", minHeight: "100vh" }}>
      <h4 className="py-3 text-center">管理選單</h4>
      <ul className="list-unstyled px-3">
        <li>
          <Button variant="link" style={{ color: "var(--light-text-color)" }} onClick={() => handleNavigation('/backstage/product_management')}>
            產品管理
          </Button>
        </li>
        <li>
          <Button variant="link" style={{ color: "var(--light-text-color)" }} onClick={() => handleNavigation('/backstage/order_management')}>
            訂單管理
          </Button>
        </li>
        <li>
          <Button variant="link" style={{ color: "var(--light-text-color)" }} onClick={() => handleNavigation('/backstage/user_management')}>
            客戶管理
          </Button>
        </li>
        <li>
          <Button variant="link" style={{ color: "var(--light-text-color)" }} onClick={() => handleNavigation('/backstage/term_management')}>
            條款管理
          </Button>
        </li>
        <li>
          <Button variant="link" style={{ color: "var(--light-text-color)" }} onClick={() => handleNavigation('/')}>
            回前台
          </Button>
        </li>
        {/* 可以根據需求擴展更多選項 */}
      </ul>
    </Col>
  );
}
