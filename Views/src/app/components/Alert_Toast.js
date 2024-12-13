"use client";  // 設定為客戶端組件

import React from "react";
import { Toast, ToastContainer } from "react-bootstrap";
import { useSelector, useDispatch } from "react-redux";
import { hideToast } from "../redux/slices/toastSlice";

const AlertToast = () => {
  const dispatch = useDispatch();
  const { message, variant, show } = useSelector((state) => state.toast);

  return (
    <ToastContainer position="top-end" className="p-3">
      <Toast
        bg={variant}
        show={show}
        onClose={() => dispatch(hideToast())}
        delay={3000}
        autohide
      >
        <Toast.Header>
          <strong className="me-auto">通知</strong>
        </Toast.Header>
        <Toast.Body className={variant === "danger" ? "text-white" : ""}>
          {message}
        </Toast.Body>
      </Toast>
    </ToastContainer>
  );
};

export default AlertToast;
