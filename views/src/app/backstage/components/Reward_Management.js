"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Table, Button, Form, Modal, InputGroup } from "react-bootstrap";
import Sidebar from "./Sidebar";
import config from "../../config";
import { useSelector } from "react-redux";

export default function RewardManagement() {
    const endpoint = config.apiBaseUrl;
    const { token } = useSelector((state) => state.user);

    const [rewardName, setRewardName] = useState("new user");
    const [loading, setLoading] = useState(true);
    const [searchReward, setSearchReward] = useState("");
    const [showModal, setShowModal] = useState(false);
    const [rewards, setRewards] = useState([]);
    const [editableReward, setEditableReward] = useState({
        id: "",
        name: "",
        description: "",
        reward_type: "",
        reward: 0,
    });
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        fetchRewards();
    }, []);

    // 獲取獎勵列表
    const fetchRewards = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${endpoint}/backstage/v1/reward_setting`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setRewards(response.data);
        } catch (error) {
            console.error("無法獲取獎勵資料：", error);
        } finally {
            setLoading(false);
        }
    };

    // 搜尋功能
    const handleSearch = (e) => {
        setSearchReward(e.target.value);
    };

    const filteredRewards = rewards.filter((reward) =>
        reward.name.toLowerCase().includes(searchReward.toLowerCase())
    );

    // 顯示新增/編輯彈出視窗
    const handleShowModal = (reward = null) => {
        if (reward) {
            setEditableReward(reward);
            setIsEditing(true);
        } else {
            setEditableReward({
                id: "",
                name: "",
                description: "",
                reward_type: "",
                reward: 0,
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

    // 新增獎勵
    const createReward = async () => {
        setLoading(true);
        try {
            await axios.post(
                `${endpoint}/backstage/v1/reward_setting`,
                {
                    name: rewardName,
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            fetchRewards()
            handleCloseModal();
        } catch (error) {
            console.error("無法新增條款：", error);
        } finally {
            setLoading(false);
            handleCloseModal();
        }
    };

    // 更新獎勵內容
    const updateReward = async () => {
        setLoading(true);
        try {
            const response = await axios.patch(
                `${endpoint}/backstage/v1/reward_setting/${editableReward.name}`,
                {
                    description: editableReward.description,
                    reward_type: editableReward.reward_type,
                    reward: editableReward.reward,
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            setRewards((prevRewards) =>
                prevRewards.map((reward) =>
                    reward.id === editableReward.id ? response.data : rewards
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
            updateReward();
        } else {
            createReward();
        }
    };

    return (
        <Container fluid>
            <Row>
                <Sidebar />
                <Col xs={10} className="p-4">
                    <h3 className="mb-4" style={{ color: "var(--primary-color)" }}>獎勵管理</h3>
                    <Row className="mb-3">
                        <Col md={6}>
                            <InputGroup>
                                <Form.Control
                                    placeholder="搜尋獎勵名稱"
                                    value={searchReward}
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
                                新增獎勵
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
                                    <th>描述</th>
                                    <th>類型</th>
                                    <th>善泰幣數量</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredRewards.map((reward) => (
                                    <tr key={reward.id}>
                                        <td>{reward.name}</td>
                                        <td>{reward.description}</td>
                                        <td>{reward.reward_type === "fixed" ? "固定數量" : "根據比例"}</td>
                                        <td>{reward.reward}</td>
                                        <td>
                                            <Button
                                                variant="link"
                                                style={{ color: "var(--accent-color)" }}
                                                onClick={() => handleShowModal(reward)}
                                            >
                                                編輯
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
                    <Modal.Title>{isEditing ? "編輯獎勵" : "新增獎勵"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        {isEditing ? <>
                            <Form.Group className="mb-3">
                                <Form.Label>名稱</Form.Label>
                                <Form.Control
                                    type="text"
                                    value={editableReward.name || ""}
                                    disabled={true}
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>描述</Form.Label>
                                <Form.Control
                                    type="text"
                                    value={editableReward.description}
                                    onChange={(e) =>
                                        setEditableReward({ ...editableReward, description: e.target.value })
                                    }
                                />
                            </Form.Group>
                            {editableReward.name === "new user" ?
                                <Form.Group className="mb-3">
                                    <Form.Label>類型</Form.Label>
                                    <Form.Select
                                        type="text"
                                        value={editableReward.reward_type}
                                        onChange={(e) =>
                                            setEditableReward({ ...editableReward, reward_type: e.target.value })
                                        }
                                    >
                                        <option value="fixed">固定數量</option>
                                    </Form.Select>
                                </Form.Group>
                                :
                                <Form.Group className="mb-3">
                                    <Form.Label>類型</Form.Label>
                                    <Form.Select
                                        type="text"
                                        value={editableReward.reward_type}
                                        onChange={(e) =>
                                            setEditableReward({ ...editableReward, reward_type: e.target.value })
                                        }
                                    >
                                        <option value="fixed">固定數量</option>
                                        <option value="ratio">根據比例</option>
                                    </Form.Select>
                                </Form.Group>
                            }

                            <Form.Group className="mb-3">
                                <Form.Label>善泰幣數量(如果選擇根據比例，請填寫0-100)</Form.Label>
                                <Form.Control
                                    type="number"
                                    value={editableReward.reward}
                                    onChange={(e) =>
                                        setEditableReward({ ...editableReward, reward: e.target.value })
                                    }
                                />
                            </Form.Group>

                        </> :
                            <Form.Group className="mb-3">
                                <Form.Label>名稱</Form.Label>
                                <Form.Select
                                    value={rewardName}
                                    onChange={(e) => setRewardName(e.target.value)}
                                >
                                    <option value="new user">新會員獎勵</option>
                                    {/*<option value="invite friend">邀請會員獎勵</option>*/}
                                </Form.Select>
                            </Form.Group>
                        }


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
