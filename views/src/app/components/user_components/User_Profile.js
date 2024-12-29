"use client";

import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button, Table, Form, Modal } from "react-bootstrap";
import { useRouter } from "next/navigation";
import axios from "axios";
import config from "../../config";
import { useSelector, useDispatch } from "react-redux";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示
import { logout, updateUserInfo } from "@/app/redux/slices/userSlice";
import { clearCart } from '@/app/redux/slices/cartSlice';
import Select from "react-select";

import { showToast } from "@/app/redux/slices/toastSlice";

export default function UserProfile() {
    const endpoint = config.apiBaseUrl;
    const router = useRouter();
    const { token, userInfo } = useSelector((state) => state.user);

    const dispatch = useDispatch();

    const [userData, setUserData] = useState({
        username: "",
        email: "",
        birth_date: "",
        mbti: "",
        phone: "",
        address: "",
    });

    const [loading, setLoading] = useState(true);
    const [editing, setEditing] = useState(false);

    const [updatedData, setUpdatedData] = useState({
        username: "",
        email: "",
        sex: "",
        birth_date: "",
        mbti: "",
        phone: "",
        address: "",
    });

    const mbtiOptions = [
        { value: "INTJ", label: "INTJ" },
        { value: "INTP", label: "INTP" },
        { value: "ENTJ", label: "ENTJ" },
        { value: "ENTP", label: "ENTP" },
        { value: "INFJ", label: "INFJ" },
        { value: "INFP", label: "INFP" },
        { value: "ENFJ", label: "ENFJ" },
        { value: "ENFP", label: "ENFP" },
        { value: "ISTJ", label: "ISTJ" },
        { value: "ISFJ", label: "ISFJ" },
        { value: "ESTJ", label: "ESTJ" },
        { value: "ESFJ", label: "ESFJ" },
        { value: "ISTP", label: "ISTP" },
        { value: "ISFP", label: "ISFP" },
        { value: "ESTP", label: "ESTP" },
        { value: "ESFP", label: "ESFP" },
    ];

    // 密碼相關狀態
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [passwordData, setPasswordData] = useState({
        new_password: "",
        confirm_password: "",
    });
    const [passwordError, setPasswordError] = useState("");

    useEffect(() => {
        fetchUserData();
    }, []);

    // 獲取用戶資料
    const fetchUserData = async () => {
        console.log(userInfo)
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
                `${endpoint}/frontstage/v1/profile`,
                updatedData,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            setUserData(response.data);
            setEditing(false);

            const userInfo = {
                "username": response.data.username,
                "sex": response.data.sex,
                "birth_date": response.data.birth_date,
                "mbti": response.data.mbti,
                "phone": response.data.phone,
                "address": response.data.address,
            }
            dispatch(updateUserInfo({ userInfo }));
        } catch (error) {
            console.error("無法更新用戶資料：", error);
        } finally {
            setLoading(false);
        }
    };

    // 修改密碼
    const handleChangePassword = async () => {
        if (passwordData.new_password !== passwordData.confirm_password) {
            setPasswordError("新密碼與確認密碼不一致");
            return;
        }
        setLoading(true);
        try {
            await axios.put(
                `${endpoint}/frontstage/v1/change-password`,
                { new_password: passwordData.new_password },
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            handleSuccess("密碼修改成功！");
            setShowPasswordModal(false);
            setPasswordData({ new_password: "", confirm_password: "" });
        } catch (error) {
            console.error("無法更新密碼：", error);
            handleError("密碼修改失敗，請重試。");
        } finally {
            setLoading(false);
        }
    };

    // 處理輸入框改變
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUpdatedData({ ...updatedData, [name]: value });
    };

    // 處理密碼輸入框改變
    const handlePasswordInputChange = (e) => {
        const { name, value } = e.target;
        setPasswordData({ ...passwordData, [name]: value });
        setPasswordError(""); // 清除錯誤訊息
    };

    // 登出功能
    const handleLogout = () => {
        dispatch(logout());
        dispatch(clearCart()); // 清空購物車
        router.push("/");
    };

    // 控制彈出視窗訊息區
    const handleSuccess = (message) => {
        dispatch(showToast({ message: message, variant: "success" }));
    };

    const handleError = (message) => {
        dispatch(showToast({ message: message, variant: "danger" }));
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
                                                value={updatedData.username}
                                                onChange={handleInputChange}
                                            />
                                        ) : (
                                            userData.username
                                        )}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Email</strong></td>
                                    <td>{updatedData.email}</td>
                                </tr>
                                <tr>
                                    <td><strong>性別</strong></td>
                                    <td>
                                        {editing ? (
                                            <Form.Select
                                                name="sex"
                                                value={updatedData.sex}
                                                onChange={handleInputChange}
                                            >
                                                <option value=""></option>
                                                <option value="男">男</option>
                                                <option value="女">女</option>
                                                <option value="其他">其他</option>
                                            </Form.Select>
                                        ) : (
                                            userData.sex
                                        )}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>出生年月日</strong></td>
                                    <td>
                                        {userData.birth_date ? (
                                            userData.birth_date
                                        ) : (
                                            <Form.Control
                                                type="date"
                                                name="birth_date"
                                                value={updatedData.birth_date || ""}
                                                onChange={handleInputChange}
                                                disabled={!!userData.birth_date} // 一旦填寫完成後禁用
                                            />
                                        )}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>MBTI</strong></td>
                                    <td>
                                        {editing ? (
                                            <Select
                                                options={mbtiOptions}
                                                value={mbtiOptions.find(option => option.value === updatedData.mbti || "")}
                                                onChange={(selectedOption) =>
                                                    setUpdatedData({ ...updatedData, mbti: selectedOption.value })
                                                }
                                                placeholder="選擇 MBTI"
                                                isSearchable
                                            />
                                        ) : (
                                            userData.mbti
                                        )}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>聯絡電話</strong></td>
                                    <td>
                                        {editing ? (
                                            <Form.Control
                                                type="text"
                                                name="phone"
                                                value={updatedData.phone}
                                                onChange={handleInputChange}
                                                placeholder="輸入聯絡電話"
                                            />
                                        ) : (
                                            userData.phone
                                        )}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>常用地址</strong></td>
                                    <td>
                                        {editing ? (
                                            <Form.Control
                                                as="textarea"
                                                name="address"
                                                value={updatedData.address}
                                                onChange={handleInputChange}
                                                placeholder="輸入常用地址"
                                            />
                                        ) : (
                                            userData.address
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
                                    onClick={handleUpdateProfile}
                                    disabled={loading}
                                >
                                    儲存
                                </Button>
                                <Button
                                    variant="secondary"
                                    onClick={() => setEditing(false)}
                                    disabled={loading}
                                    className="me-2"
                                >
                                    取消
                                </Button>
                            </>
                        ) : (
                            <>
                                <Button
                                    variant="primary"
                                    className="me-2"
                                    onClick={() => setEditing(true)}
                                >
                                    修改資料
                                </Button>
                                <Button variant="warning" className="me-2" onClick={() => setShowPasswordModal(true)}>
                                    修改密碼
                                </Button>
                            </>

                        )}
                        <Button variant="danger" onClick={handleLogout}>
                            登出
                        </Button>
                    </div>
                </Col>
            </Row>

            {/* 修改密碼彈出視窗 */}
            <Modal show={showPasswordModal} onHide={() => setShowPasswordModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>修改密碼</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group controlId="newPassword" className="mb-3">
                            <Form.Label>新密碼</Form.Label>
                            <Form.Control
                                type="password"
                                name="new_password"
                                value={passwordData.new_password}
                                onChange={handlePasswordInputChange}
                                placeholder="輸入新密碼"
                            />
                        </Form.Group>
                        <Form.Group controlId="confirmPassword" className="mb-3">
                            <Form.Label>確認新密碼</Form.Label>
                            <Form.Control
                                type="password"
                                name="confirm_password"
                                value={passwordData.confirm_password}
                                onChange={handlePasswordInputChange}
                                placeholder="再次輸入新密碼"
                            />
                        </Form.Group>
                        {passwordError && <p className="text-danger">{passwordError}</p>}
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowPasswordModal(false)}>
                        取消
                    </Button>
                    <Button variant="primary" onClick={handleChangePassword}>
                        確認修改
                    </Button>
                </Modal.Footer>
            </Modal>
        </Container>
    );
}
