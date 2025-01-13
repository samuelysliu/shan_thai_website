// src/app/components/Sidebar.js
"use client";

import React, { useState } from "react";
import { Col, Button } from 'react-bootstrap';
import { useRouter } from 'next/navigation';
import { FaChevronLeft, FaChevronRight } from "react-icons/fa"; // 引入 Icon


export default function Sidebar() {
  const router = useRouter();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleNavigation = (path) => {
    router.push(path);
  };

  const toggleSidebar = () => {
    setIsCollapsed((prev) => !prev);
  };

  return (
    <Col
      xs={isCollapsed ? 1 : 2} // 動態調整寬度
      className={`sidebar ${isCollapsed ? "collapsed" : ""}`}
    >
      <div className="sidebar-header">
        {!isCollapsed && <h4 className="py-3 text-center">管理選單</h4>}
        <Button
          variant="link"
          className="toggle-btn"
          onClick={toggleSidebar}
        >
          {isCollapsed ? <FaChevronRight /> : <FaChevronLeft />}
        </Button>
      </div>
      {!isCollapsed && (
        <ul>
          <li>
            <Button
              variant="link"
              className="text-light"
              onClick={() => handleNavigation("/backstage/product_management")}
            >
              產品管理
            </Button>
          </li>
          <li>
            <Button
              variant="link"
              className="text-light"
              onClick={() => handleNavigation("/backstage/order_management")}
            >
              訂單管理
            </Button>
          </li>
          <li>
            <Button
              variant="link"
              className="text-light"
              onClick={() => handleNavigation("/backstage/user_management")}
            >
              客戶管理
            </Button>
          </li>
          <li>
            <Button
              variant="link"
              className="text-light"
              onClick={() => handleNavigation("/backstage/term_management")}
            >
              條款管理
            </Button>
          </li>
          <li>
            <Button
              variant="link"
              className="text-light"
              onClick={() => handleNavigation("/backstage/reward_management")}
            >
              獎勵管理
            </Button>
          </li>
          <li>
            <Button
              variant="link"
              className="text-light"
              onClick={() => handleNavigation("/")}
            >
              回前台
            </Button>
          </li>
        </ul>
      )}
    </Col>
  );
}
