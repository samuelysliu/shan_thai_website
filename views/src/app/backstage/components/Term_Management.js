"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Table, Button, Form, Modal, InputGroup } from "react-bootstrap";
import Sidebar from "./Sidebar";
import config from "../../config";
import { useSelector } from "react-redux";
import TextEditor from "./Text_Editor";

export default function TermManagement() {
    const endpoint = config.apiBaseUrl;
    const { token } = useSelector((state) => state.user);

    const [terms, setTerms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [showModal, setShowModal] = useState(false);
    const [editableTerm, setEditableTerm] = useState({
        tid: null,
        name: "",
        content: "", // TinyMCE 內容初始化為空字串
        version: "",
    });
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        fetchTerms();
    }, []);

    // 獲取條款列表
    const fetchTerms = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${endpoint}/backstage/v1/terms`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setTerms(response.data);
        } catch (error) {
            console.error("無法獲取條款資料：", error);
        } finally {
            setLoading(false);
        }
    };

    // 搜尋功能
    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
    };

    const filteredTerms = terms.filter((term) =>
        term.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // 顯示新增/編輯彈出視窗
    const handleShowModal = (term = null) => {
        if (term) {
            setEditableTerm(term);
            setIsEditing(true);
        } else {
            setEditableTerm({
                tid: null,
                name: "",
                content: "",
                version: "",
            });
            setIsEditing(false);
        }
        setShowModal(true);
    };

    // 關閉彈出視窗
    const handleCloseModal = () => {
        setShowModal(false);
        setIsEditing(false);
    };

    // 新增條款
    const createTerm = async () => {
        setLoading(true);
        try {
            const response = await axios.post(
                `${endpoint}/backstage/v1/terms`,
                {
                    name: editableTerm.name,
                    content: editableTerm.content, // 保存 TinyMCE 編輯器內容
                    version: editableTerm.version,
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setTerms([...terms, response.data]);
            handleCloseModal();
        } catch (error) {
            console.error("無法新增條款：", error);
        } finally {
            setLoading(false);
        }
    };

    // 更新條款
    const updateTerm = async () => {
        setLoading(true);
        try {
            const response = await axios.patch(
                `${endpoint}/backstage/v1/terms/${editableTerm.tid}`,
                {
                    name: editableTerm.name,
                    content: editableTerm.content,
                    version: editableTerm.version,
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            setTerms((prevTerms) =>
                prevTerms.map((term) =>
                    term.tid === editableTerm.tid ? response.data : term
                )
            );
            handleCloseModal();
        } catch (error) {
            console.error("無法更新條款：", error);
        } finally {
            setLoading(false);
        }
    };

    // 表單提交
    const handleSubmit = () => {
        if (isEditing) {
            updateTerm();
        } else {
            createTerm();
        }
    };

    return (
        <Container fluid>
            <Row>
                <Sidebar />
                <Col xs={10} className="p-4">
                    <h3 className="mb-4" style={{ color: "var(--primary-color)" }}>條款管理</h3>
                    <Row className="mb-3">
                        <Col md={6}>
                            <InputGroup>
                                <Form.Control
                                    placeholder="搜尋條款名稱"
                                    value={searchTerm}
                                    onChange={handleSearch}
                                />
                            </InputGroup>
                        </Col>
                        <Col md={6} className="text-end">
                            <Button
                                variant="primary"
                                style={{ backgroundColor: "var(--accent-color)", borderColor: "var(--accent-color)" }}
                                onClick={() => handleShowModal()}
                            >
                                新增條款
                            </Button>
                        </Col>
                    </Row>
                    {loading ? (
                        <p>Loading...</p>
                    ) : (
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>名稱</th>
                                    <th>版本</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredTerms.map((term) => (
                                    <tr key={term.tid}>
                                        <td>{term.name}</td>
                                        <td>{term.version}</td>
                                        <td>
                                            <Button
                                                variant="link"
                                                style={{ color: "var(--accent-color)" }}
                                                onClick={() => handleShowModal(term)}
                                            >
                                                編輯
                                            </Button>
                                            <Button
                                                variant="link"
                                                style={{ color: "var(--danger-color)" }}
                                                onClick={() => deleteTerm(term.tid)}
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

            {/* 新增/編輯條款彈出視窗 */}
            <Modal show={showModal} onHide={handleCloseModal} className="backstage">
                <Modal.Header closeButton>
                    <Modal.Title>{isEditing ? "編輯條款" : "新增條款"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>名稱</Form.Label>
                            <Form.Control
                                type="text"
                                value={editableTerm.name}
                                onChange={(e) =>
                                    setEditableTerm({ ...editableTerm, name: e.target.value })
                                }
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>內容</Form.Label>
                            <TextEditor
                                value={editableTerm.content}
                                onChange={(content) =>
                                    setEditableTerm({ ...editableTerm, content })
                                }
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>版本</Form.Label>
                            <Form.Control
                                type="text"
                                value={editableTerm.version}
                                onChange={(e) =>
                                    setEditableTerm({ ...editableTerm, version: e.target.value })
                                }
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
                        onClick={handleSubmit}
                        style={{
                            backgroundColor: "var(--accent-color)",
                            borderColor: "var(--accent-color)",
                        }}
                    >
                        儲存
                    </Button>
                </Modal.Footer>
            </Modal>
        </Container>
    );
}
