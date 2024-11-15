"use client";

import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { useRouter } from 'next/navigation';

export default function LoginModal({ show, handleClose }) {
  const router = useRouter();
  const [form, setForm] = useState({ email: '', password: '' });

  const handleGoogleSuccess = (credentialResponse) => {
    console.log("Google JWT:", credentialResponse.credential);
    // 可以將 JWT 發送到後端 API 進行驗證
    router.push("/dashboard");
  };

  const handleGoogleFailure = () => {
    console.error("Google 登入失敗");
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // 此處執行一般登入/註冊邏輯
    console.log("Email:", form.email, "Password:", form.password);
    router.push("/dashboard"); 
  };

  return (
    <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>會員登入 / 註冊</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {/* Google 第三方登入按鈕 */}
          <div className="d-flex justify-content-center mb-3">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleFailure}
            />
          </div>
          <hr />
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formEmail" className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={form.email}
                onChange={handleFormChange}
                placeholder="輸入電子郵件"
                required
              />
            </Form.Group>
            <Form.Group controlId="formPassword" className="mb-3">
              <Form.Label>密碼</Form.Label>
              <Form.Control
                type="password"
                name="password"
                value={form.password}
                onChange={handleFormChange}
                placeholder="輸入密碼"
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100">
              登入 / 註冊
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </GoogleOAuthProvider>
  );
}
