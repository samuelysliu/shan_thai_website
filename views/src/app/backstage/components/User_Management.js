"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Table, Button, Form, InputGroup, Modal } from "react-bootstrap";
import Sidebar from "./Sidebar";
import config from "../../config";

import { useSelector } from 'react-redux';

export default function UserManagement() {
    const endpoint = config.apiBaseUrl;

    // 從 Redux 中取出會員資訊
    const { token } = useSelector((state) => state.user);

    const [searchTerm, setSearchTerm] = useState("");
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    // 控制彈出視窗顯示
    const [showModal, setShowModal] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [currentUser, setCurrentUser] = useState({
        uid: null,
        email: "",
        password: "",
        username: "",
        sex: "",
        star: 0,
        identity: "",
        note: "",
    });

    useEffect(() => {
        fetchUsers();
    }, []);

    // 從後端拉取使用者資料
    const fetchUsers = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${endpoint}/backstage/v1/users`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            });
            setUsers(response.data); // 從後端獲取使用者資料
        } catch (error) {
            console.error("無法拉取使用者資料：", error);
        } finally {
            setLoading(false);
        }
    };

    // 新增使用者
    const createUser = async () => {
        setLoading(true);
        try {
            const response = await axios.post(`${endpoint}/backstage/v1/users`, currentUser, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            });
            setUsers((prevUsers) => [...prevUsers, response.data]); // 新增成功後更新使用者列表
            handleCloseModal();
        } catch (error) {
            console.error("無法新增使用者：", error);
        } finally {
            setLoading(false);
        }
    };

    // 修改使用者資料
    const updateUser = async () => {
        setLoading(true);
        try {
            const response = await axios.patch(`${endpoint}/backstage/v1/users/${currentUser.uid}`, currentUser, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            });
            setUsers((prevUsers) =>
                prevUsers.map((user) => (user.uid === response.data.uid ? response.data : user))
            ); // 更新成功後更新列表
            handleCloseModal();
        } catch (error) {
            console.error("無法更新使用者資料：", error);
        } finally {
            setLoading(false);
        }
    };

    // 刪除使用者
    const deleteUser = async (uid) => {
        setLoading(true);
        try {
            await axios.delete(`${endpoint}/backstage/v1/users/${uid}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            });
            setUsers((prevUsers) => prevUsers.filter((user) => user.uid !== uid)); // 刪除成功後移除
        } catch (error) {
            console.error("無法刪除使用者：", error);
        } finally {
            setLoading(false);
        }
    };

    // 搜尋功能
    const handleSearch = (e) => setSearchTerm(e.target.value);

    const filteredUsers = users.filter((user) =>
        user.username.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // 彈出視窗控制
    const handleShowModal = (user = null) => {
        if (user) {
            setIsEditing(true);
            setCurrentUser(user);
        } else {
            setIsEditing(false);
            setCurrentUser({
                uid: null,
                email: "",
                username: "",
                sex: "",
                star: 0,
                identity: "",
                note: "",
            });
        }
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setCurrentUser({
            uid: null,
            email: "",
            username: "",
            sex: "",
            star: 0,
            identity: "",
            note: "",
        });
    };

    return (
        <Container fluid>
            <Row>
                <Sidebar />
                <Col xs={10} className="p-4">
                    <h3 className="mb-4" style={{ color: "var(--primary-color)" }}>客戶管理</h3>

                    {/* 搜尋 */}
                    <Row className="mb-3">
                        <Col md={6}>
                            <InputGroup>
                                <Form.Control
                                    placeholder="搜尋使用者名稱"
                                    value={searchTerm}
                                    onChange={handleSearch}
                                />
                            </InputGroup>
                        </Col>
                        <Col md={2}>
                            <Button
                                variant="primary"
                                style={{ backgroundColor: "var(--accent-color)", borderColor: "var(--accent-color)" }}
                                onClick={() => handleShowModal()}
                            >
                                新增使用者
                            </Button>
                        </Col>
                    </Row>

                    {/* 使用者列表 */}
                    {loading ? (
                        <p>Loading...</p>
                    ) : (
                        <Table striped bordered hover>
                            <thead style={{ backgroundColor: "var(--primary-color)", color: "var(--light-text-color)" }}>
                                <tr>
                                    <th>使用者編號</th>
                                    <th>Email</th>
                                    <th>名稱</th>
                                    <th>性別</th>
                                    <th>星數</th>
                                    <th>身份</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredUsers.map((user) => (
                                    <tr key={user.uid}>
                                        <td>{user.uid}</td>
                                        <td>{user.email}</td>
                                        <td>{user.username}</td>
                                        <td>{user.sex || "未指定"}</td>
                                        <td>{user.star}</td>
                                        <td>{user.identity || "未指定"}</td>
                                        <td>
                                            <Button
                                                variant="link"
                                                style={{ color: "var(--accent-color)" }}
                                                onClick={() => handleShowModal(user)}
                                            >
                                                編輯
                                            </Button>
                                            |
                                            <Button
                                                variant="link"
                                                style={{ color: "var(--secondary-color)" }}
                                                onClick={() => deleteUser(user.uid)}
                                            >
                                                刪除
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    )}
                </Col>
            </Row>

            {/* 新增/編輯使用者的彈出視窗 */}
            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>{isEditing ? "編輯使用者" : "新增使用者"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                type="email"
                                value={currentUser.email}
                                onChange={(e) => setCurrentUser({ ...currentUser, email: e.target.value })}
                                disabled={isEditing} // 編輯時不可更改 Email
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>password</Form.Label>
                            <Form.Control
                                type="text"
                                value={currentUser.password}
                                onChange={(e) => setCurrentUser({ ...currentUser, password: e.target.value })}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>名稱</Form.Label>
                            <Form.Control
                                type="text"
                                value={currentUser.username}
                                onChange={(e) => setCurrentUser({ ...currentUser, username: e.target.value })}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>性別</Form.Label>
                            <Form.Select
                                value={currentUser.sex || ""}
                                onChange={(e) => setCurrentUser({ ...currentUser, sex: e.target.value })}
                            >
                                <option value="">未指定</option>
                                <option value="男">男</option>
                                <option value="女">女</option>
                            </Form.Select>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>星數</Form.Label>
                            <Form.Control
                                type="number"
                                value={currentUser.star}
                                onChange={(e) => setCurrentUser({ ...currentUser, star: e.target.value })}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>備註</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                value={currentUser.note || ""}
                                onChange={(e) => setCurrentUser({ ...currentUser, note: e.target.value })}
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleCloseModal}>
                        取消
                    </Button>
                    <Button
                        variant="primary"
                        style={{ backgroundColor: "var(--accent-color)", borderColor: "var(--accent-color)" }}
                        onClick={isEditing ? updateUser : createUser}
                    >
                        {isEditing ? "儲存修改" : "新增"}
                    </Button>
                </Modal.Footer>
            </Modal>
        </Container>
    );
}
