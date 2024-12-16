"use client";

import React, { useEffect, useState } from 'react';
import { Modal, Button, Form, Col } from 'react-bootstrap';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { useRouter } from 'next/navigation';
import config from "../../config";
import axios from "axios";
import { useDispatch } from "react-redux";
import { login } from '../../redux/slices/userSlice';

export default function LoginModal({ show, handleClose }) {
  const endpoint = config.apiBaseUrl;
  const router = useRouter();
  const dispatch = useDispatch();

  const [form, setForm] = useState({ email: '', password: '' });
  const [message, setMessage] = useState("");

  const googleClientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  // 處理Google 登入、註冊
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // 將 Google JWT 傳送到後端進行驗證
      const response = await axios.post(`${endpoint}/frontstage/v1/login/google`, {
        token: credentialResponse.credential,
      });

      const responseData = response.data.detail
      const userInfo = { "uid": responseData.uid, "email": responseData.email, "username": responseData.username, "sex": responseData.sex, "isAdmin": responseData.isAdmin }
      const token = responseData.token;
      dispatch(login({ userInfo, token }));

      handleClose();
      router.push("/");
    } catch (err) {
      console.error("Google login failed:", err);
      setError("Google 登入失敗，請稍後再試");
    }
  };

  const handleGoogleFailure = () => {
    console.error("Google 登入失敗");
    setError("Google 登入失敗，請稍後再試");
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // 處理一般登入
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${endpoint}/frontstage/v1/login`, form);
      const responseData = response.data.detail
      const userInfo = { "uid": responseData.uid, "email": responseData.email, "username": responseData.username, "sex": responseData.sex, "isAdmin": responseData.isAdmin }
      const token = responseData.token;
      dispatch(login({ userInfo, token }));

      handleClose();
      router.push("/");
    } catch (err) {
      setError("登入失敗，請檢查帳號或密碼");
    }
  };

  // 處理一般註冊
  const handleRegister = async () => {
    try {
      const response = await axios.post(`${endpoint}/frontstage/v1/register`, {
        email: form.email,
        password: form.password,
      });

      setMessage(response.data.detail === "Email is already registered"
        ? "此 Email 已經註冊過了！"
        : "註冊成功，請登入！");
    } catch (err) {
      console.log(err)
      setMessage("註冊失敗，請確認資料是否正確");
    }
  };

  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <Modal className="login-modal" show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>會員登入</Modal.Title>
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
          <Form onSubmit={handleLoginSubmit}>
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
            {message && <p className="text-danger text-center">{message}</p>}
            <Button type="submit" className="button-primary w-100">
              登入
            </Button>
            <Button
              className="button-secondary w-100 mt-2"
              onClick={handleRegister}
            >
              註冊
            </Button>

          </Form>
        </Modal.Body>
        <Modal.Footer className="login-modal-footer">
          <Col><a>忘記密碼了嗎？</a></Col>
        </Modal.Footer>
      </Modal>
    </GoogleOAuthProvider>
  );
}
