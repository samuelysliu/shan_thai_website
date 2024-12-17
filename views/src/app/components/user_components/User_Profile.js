"use client";

import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button, Table, Form } from "react-bootstrap";
import { useRouter } from "next/navigation";
import axios from "axios";
import config from "../../config";
import { useSelector } from "react-redux";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示

export default function UserProfile() {
    const endpoint = config.apiBaseUrl;
    const router = useRouter();
    const { token, userInfo } = useSelector((state) => state.user);

    const [userData, setUserData] = useState({
        username: "",
        email: "",
    });

    const [editableData, setEditableData] = useState({});
    const [loading, setLoading] = useState(true);
    const [editing, setEditing] = useState(false);

    const [updatedData, setUpdatedData] = useState({
        username: "",
        email: "",
    });
    const [passwordData, setPasswordData] = useState({
        old_password: "",
        new_password: "",
    });

    useEffect(() => {
        fetchUserData();
    }, []);

    // 獲取用戶資料
    const fetchUserData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${endpoint}/frontstage/v1/profile`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setUserData(response.data);
            setUpdatedData(response.data);
        } catch (error) {
            console.error("無法獲取用戶資料：", error);
        } finally {
            setLoading(false);
        }
    };

    // 修改資料
    const handleUpdateProfile = async () => {
        setLoading(true);
        try {
            const response = await axios.put(
                `${endpoint}/profile`,
                updatedData,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            setUserData(response.data);
            setShowEditModal(false);
        } catch (error) {
            console.error("無法更新用戶資料：", error);
        } finally {
            setLoading(false);
        }
    };

    // 修改密碼
    const handleChangePassword = async () => {
        setLoading(true);
        try {
            await axios.put(
                `${endpoint}/change-password`,
                passwordData,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            setShowPasswordModal(false);
            setPasswordData({ old_password: "", new_password: "" });
        } catch (error) {
            console.error("無法更新密碼：", error);
        } finally {
            setLoading(false);
        }
    };

    // 處理輸入框改變
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setEditableData({ ...editableData, [name]: value });
    };

    // 登出功能
    const handleLogout = () => {
        dispatch(logout()); // 清空 Redux 狀態
        router.push("/"); // 返回首頁
    };

    return (
        <Container fluid>
            <Row className="my-3">
                <Col xs={12}>
                    <Button variant="link" onClick={() => router.push("/")}>
                        <FaArrowLeft /> 返回
                    </Button>
                </Col>
            </Row>
            <Row className="justify-content-center">
                <Col xs={10} md={8} lg={6}>
                    <h3 className="mb-4 text-center">使用者資料</h3>
                    {loading ? (
                        <p>載入中...</p>
                    ) : (
                        <Table bordered hover className="table-modern">
                            <tbody>
                                <tr>
                                    <td><strong>用戶名稱</strong></td>
                                    <td>
                                        {editing ? (
                                            <Form.Control
                                                type="text"
                                                name="username"
                                                value={editableData.username}
                                                onChange={handleInputChange}
                                            />
                                        ) : (
                                            userData.username
                                        )}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Email</strong></td>
                                    <td>
                                        {editing ? (
                                            <Form.Control
                                                type="email"
                                                name="email"
                                                value={editableData.email}
                                                onChange={handleInputChange}
                                            />
                                        ) : (
                                            userData.email
                                        )}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>性別</strong></td>
                                    <td>
                                        {editing ? (
                                            <Form.Select
                                                name="sex"
                                                value={editableData.sex}
                                                onChange={handleInputChange}
                                            >
                                                <option value="male">男</option>
                                                <option value="female">女</option>
                                                <option value="other">其他</option>
                                            </Form.Select>
                                        ) : (
                                            userData.sex
                                        )}
                                    </td>
                                </tr>
                            </tbody>
                        </Table>
                    )}
                    <div className="text-center mt-3">
                        {editing ? (
                            <>
                                <Button
                                    variant="primary"
                                    className="me-2"
                                    onClick={handleSave}
                                    disabled={loading}
                                >
                                    儲存
                                </Button>
                                <Button
                                    variant="secondary"
                                    onClick={() => setEditing(false)}
                                    disabled={loading}
                                >
                                    取消
                                </Button>
                            </>
                        ) : (
                            <Button
                                variant="primary"
                                className="me-2"
                                onClick={() => setEditing(true)}
                            >
                                修改資料
                            </Button>
                        )}
                        <Button variant="danger" onClick={handleLogout}>
                            登出
                        </Button>
                    </div>
                </Col>
            </Row>
        </Container>
    );
}
