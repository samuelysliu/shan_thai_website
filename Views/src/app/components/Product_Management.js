// src/app/components/ProductManagement.js
"use client";

import React, { useState } from 'react';
import { Container, Row, Col, Table, Button, Form, InputGroup, Modal } from 'react-bootstrap';
import Sidebar from './Sidebar';

export default function ProductManagement() {
    const [searchTerm, setSearchTerm] = useState("");
    const [filter, setFilter] = useState("all");
    const [products, setProducts] = useState([
        { id: 1, name: "產品A", price: 500, category: "分類一", description: "描述A", stock: 10, images: [] },
        { id: 2, name: "產品B", price: 1000, category: "分類二", description: "描述B", stock: 5, images: [] },
        { id: 3, name: "產品C", price: 750, category: "分類一", description: "描述C", stock: 8, images: [] },
    ]);

    // 控制彈出視窗顯示
    const [showModal, setShowModal] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [currentProduct, setCurrentProduct] = useState({
        id: null,
        images: [],
        title: "",
        description: "",
        price: "",
        stock: "",
    });

    const handleSearch = (e) => setSearchTerm(e.target.value);
    const handleFilterChange = (e) => setFilter(e.target.value);

    // 彈出視窗相關操作
    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => {
        setShowModal(false);
        setIsEditing(false);
        setCurrentProduct({ id: null, images: [], title: "", description: "", price: "", stock: "" });
    };

    const handleProductChange = (e) => {
        const { name, value } = e.target;
        setCurrentProduct((prev) => ({ ...prev, [name]: value }));
    };

    const handleImageUpload = (e) => {
        const files = Array.from(e.target.files);
        setCurrentProduct((prev) => ({ ...prev, images: [...prev.images, ...files] }));
    };

    const handleAddProduct = () => {
        const newId = products.length + 1;
        const newProduct = { ...currentProduct, id: newId };
        setProducts([...products, newProduct]);
        handleCloseModal();
    };

    const handleEditProduct = (product) => {
        setIsEditing(true);
        setCurrentProduct({
            id: product.id,
            images: product.images,
            title: product.name,
            description: product.description,
            price: product.price,
            stock: product.stock,
        });
        handleShowModal();
    };

    const handleSaveChanges = () => {
        setProducts(products.map((product) =>
            product.id === currentProduct.id ? { ...product, ...currentProduct, name: currentProduct.title } : product
        ));
        handleCloseModal();
    };

    const filteredProducts = products.filter(product => {
        return (
            (filter === "all" || product.category === filter) &&
            product.name.toLowerCase().includes(searchTerm.toLowerCase())
        );
    });

    return (
        <Container fluid>
            <Row>
                <Sidebar />
                {/* 主要內容 */}
                <Col xs={10} className="p-4">
                    <h3 className="mb-4" style={{ color: "var(--primary-color)" }}>產品管理</h3>

                    {/* 搜尋和篩選 */}
                    <Row className="mb-3">
                        <Col md={6}>
                            <InputGroup>
                                <Form.Control
                                    placeholder="搜尋產品名稱"
                                    value={searchTerm}
                                    onChange={handleSearch}
                                />
                            </InputGroup>
                        </Col>
                        <Col md={4}>
                            <Form.Select onChange={handleFilterChange} value={filter}>
                                <option value="all">所有分類</option>
                                <option value="分類一">分類一</option>
                                <option value="分類二">分類二</option>
                            </Form.Select>
                        </Col>
                        <Col md={2}>
                            <Button variant="primary" style={{ backgroundColor: "var(--accent-color)", borderColor: "var(--accent-color)" }} onClick={handleShowModal}>
                                新增產品
                            </Button>
                        </Col>
                    </Row>

                    {/* 產品表格 */}
                    <Table striped bordered hover>
                        <thead style={{ backgroundColor: "var(--primary-color)", color: "var(--light-text-color)" }}>
                            <tr>
                                <th>產品編號</th>
                                <th>產品名稱</th>
                                <th>價格</th>
                                <th>分類</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredProducts.map(product => (
                                <tr key={product.id}>
                                    <td>{product.id}</td>
                                    <td>{product.name}</td>
                                    <td>NT. {product.price}</td>
                                    <td>{product.category}</td>
                                    <td>
                                        <Button variant="link" style={{ color: "var(--accent-color)" }} onClick={() => handleEditProduct(product)}>編輯</Button> |
                                        <Button variant="link" style={{ color: "var(--secondary-color)" }}>刪除</Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </Col>
            </Row>

            {/* 新增/編輯產品的彈出視窗 */}
            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>{isEditing ? "編輯產品" : "新增產品"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>圖片上傳</Form.Label>
                            <Form.Control type="file" multiple onChange={handleImageUpload} />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>標題</Form.Label>
                            <Form.Control
                                type="text"
                                name="title"
                                value={currentProduct.title}
                                onChange={handleProductChange}
                                placeholder="輸入產品標題"
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>產品說明</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                name="description"
                                value={currentProduct.description}
                                onChange={handleProductChange}
                                placeholder="輸入產品說明"
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>價格</Form.Label>
                            <Form.Control
                                type="number"
                                name="price"
                                value={currentProduct.price}
                                onChange={handleProductChange}
                                placeholder="輸入價格"
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>剩餘數量</Form.Label>
                            <Form.Control
                                type="number"
                                name="stock"
                                value={currentProduct.stock}
                                onChange={handleProductChange}
                                placeholder="輸入剩餘數量"
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
                        onClick={isEditing ? handleSaveChanges : handleAddProduct}
                    >
                        {isEditing ? "儲存修改" : "新增"}
                    </Button>
                </Modal.Footer>
            </Modal>
        </Container>
    );
}
