"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Table, Button, Form, InputGroup, Modal } from "react-bootstrap";
import Sidebar from "../../components/Sidebar";
import config from "../../config";

export default function ProductManagement() {
    let endpoint = config.apiBaseUrl;

    const [searchTerm, setSearchTerm] = useState("");
    const [filter, setFilter] = useState("all");
    const [products, setProducts] = useState([]); // 初始化為空陣列
    const [loading, setLoading] = useState(true);

    // 控制彈出視窗顯示
    const [showModal, setShowModal] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [currentProduct, setCurrentProduct] = useState({
        pid: null,
        title_cn: "",
        content_cn: "",
        price: "",
        remain: "",
        productTag: "",
        productImageUrl: "",
    });
    const [productTags, setProductTags] = useState([]);

    useEffect(() => {
        fetchProducts();
        fetchTags();
    }, []);

    // 從後端拉取產品列表
    const fetchProducts = async () => {
        setLoading(true);
        try {
            const response = await axios.get(endpoint + "/backstage/v1/product");
            setProducts(response.data); // 更新產品列表
        } catch (error) {
            console.error("無法拉取產品列表：", error);
        } finally {
            setLoading(false);
        }
    };

    // 刪除指定產品
    const deleteProducts = async (pid) => {
        setLoading(true);
        try {
            const response = await axios.delete(endpoint + "/backstage/v1/product/" + pid);
            setProducts(products.filter(product => product.pid !== pid)); // 更新產品列表
        } catch (error) {
            console.error("無法刪除該產品：", error);
        } finally {
            setLoading(false);
        }
    }

    // 新增產品
    const createProducts = async () => {
        setLoading(true);
        try {
            const formData = new FormData();
            formData.append("title_cn", currentProduct.title_cn);
            formData.append("content_cn", currentProduct.content_cn);
            formData.append("price", currentProduct.price);
            formData.append("remain", currentProduct.remain)
            if (currentProduct.productImageFile) {
                formData.append("file", currentProduct.productImageFile); // 圖片檔案
            }

            const response = await axios.post(endpoint + "/backstage/v1/product",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });
            const newProduct = response.data;
            setProducts((prevProducts) => [...prevProducts, newProduct]);
            handleCloseModal();
        } catch (error) {
            console.error("無法新增產品：", error);
        } finally {
            setLoading(false);
        }
    }

    // 修改產品內容
    const updateProducts = async () => {
        const formData = new FormData();
        if (currentProduct.title_cn) formData.append("title_cn", currentProduct.title_cn);
        if (currentProduct.content_cn) formData.append("content_cn", currentProduct.content_cn);
        if (currentProduct.price) formData.append("price", currentProduct.price);
        if (currentProduct.remain) formData.append("remain", currentProduct.remain);

        // 判斷是否需要上傳圖片
        if (currentProduct.productImageFile) {
            // 若使用者上傳新圖片
            formData.append("file", currentProduct.productImageFile);
        } else if (currentProduct.productImageUrl) {
            // 若圖片未變更，傳遞圖片 URL
            formData.append("productImageUrl", currentProduct.productImageUrl);
        }
        try {
            const response = await axios.patch(endpoint + "/backstage/v1/product/" + currentProduct.pid,
                formData,
                {
                    headers: { "Content-Type": "multipart/form-data" },
                }
            );

            const updatedProduct = response.data;

            // 更新本地產品列表
            setProducts((prevProducts) =>
                prevProducts.map((product) =>
                    product.pid === updatedProduct.pid ? updatedProduct : product
                )
            );
            handleCloseModal(); // 關閉彈窗
        } catch (error) {
            console.error("Failed to update product:", error);
        } finally {
            setLoading(false);
        }
    }

    // 從後端拉取產品標籤列表
    const fetchTags = async () => {
        try {
            const response = await axios.get(endpoint + "/backstage/v1/product_tag");
            setProductTags(response.data); // 更新產品列表
        } catch (error) {
            console.error("無法拉取產品列表：", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (e) => setSearchTerm(e.target.value);

    const filteredProducts = products.filter((product) => {
        const title = product.title_cn || ""; // 預設為空字串
        return (
            (filter === "all" || product.category === filter) &&
            title.toLowerCase().includes(searchTerm.toLowerCase())
        );
    });

    // 彈出視窗相關操作
    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => {
        setShowModal(false);
        setIsEditing(false);
        setCurrentProduct({
            pid: null,
            title_cn: "",
            content_cn: "",
            price: "",
            remain: "",
            productTag: "",
            productImageUrl: "",
        });
    };

    // 點擊編輯按鈕時的處理
    const handleEditProduct = (product) => {
        setIsEditing(true);
        setCurrentProduct(product); // 設置為當前產品
        setShowModal(true);
    };

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
                            <Form.Select
                                value={currentProduct.productTag || ""}
                                onChange={(e) =>
                                    setCurrentProduct({
                                        ...currentProduct,
                                        productTag: e.target.value,
                                    })
                                }
                            >
                                <option value="">請選擇標籤</option>
                                {productTags.map((tag) => (
                                    <option key={tag.ptid} value={tag.productTag}>
                                        {tag.productTag}
                                    </option>
                                ))}
                            </Form.Select>
                        </Col>
                        <Col md={2}>
                            <Button
                                variant="primary"
                                style={{ backgroundColor: "var(--accent-color)", borderColor: "var(--accent-color)" }}
                                onClick={handleShowModal}
                            >
                                新增產品
                            </Button>
                        </Col>
                    </Row>

                    {/* Loading 狀態 */}
                    {loading ? (
                        <p>Loading...</p>
                    ) : (
                        <Table striped bordered hover>
                            <thead style={{ backgroundColor: "var(--primary-color)", color: "var(--light-text-color)" }}>
                                <tr>
                                    <th>產品編號</th>
                                    <th>產品名稱</th>
                                    <th>價格</th>
                                    <th>剩餘數量</th>
                                    <th>產品標籤</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredProducts.map((product) => (
                                    <tr key={product.pid}>
                                        <td>{product.pid}</td>
                                        <td>{product.title_cn}</td>
                                        <td>NT. {product.price}</td>
                                        <td>{product.remain}</td>
                                        <td>{product.productTag}</td>
                                        <td>
                                            <Button
                                                variant="link"
                                                style={{ color: "var(--accent-color)" }}
                                                onClick={() => handleEditProduct(product)}
                                            >
                                                編輯
                                            </Button>
                                            |
                                            <Button
                                                variant="link"
                                                style={{ color: "var(--secondary-color)" }}
                                                onClick={() => deleteProducts(product.pid)}
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

            {/* 新增/編輯產品的彈出視窗 */}
            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>{isEditing ? "編輯產品" : "新增產品"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>產品名稱</Form.Label>
                            <Form.Control
                                type="text"
                                value={currentProduct.title_cn}
                                name="title_cn"
                                onChange={(e) =>
                                    setCurrentProduct({ ...currentProduct, title_cn: e.target.value })
                                }
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>產品說明</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                value={currentProduct.content_cn}
                                name="content_cn"
                                onChange={(e) =>
                                    setCurrentProduct({ ...currentProduct, content_cn: e.target.value })
                                }
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>價格</Form.Label>
                            <Form.Control
                                type="number"
                                value={currentProduct.price}
                                name="price"
                                onChange={(e) =>
                                    setCurrentProduct({ ...currentProduct, price: e.target.value })
                                }
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>剩餘數量</Form.Label>
                            <Form.Control
                                type="number"
                                value={currentProduct.remain}
                                name="remain"
                                onChange={(e) =>
                                    setCurrentProduct({ ...currentProduct, remain: e.target.value })
                                }
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>產品標籤</Form.Label>
                            <Form.Select
                                value={currentProduct.productTag}
                                onChange={(e) =>
                                    setCurrentProduct({ ...currentProduct, productTag: e.target.value })
                                }
                            >
                                <option value="">請選擇標籤</option>
                                {productTags.map((tag) => (
                                    <option key={tag.ptid} value={tag.productTag}>
                                        {tag.productTag}
                                    </option>
                                ))}
                            </Form.Select>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>圖片上傳</Form.Label>
                            <Form.Control
                                type="file"
                                onChange={(e) => {
                                    const file = e.target.files[0];
                                    if (file) {
                                        const fileType = file.type;
                                        // 確認檔案類型是否正確
                                        if (fileType === "image/jpeg" || fileType === "image/png") {
                                            setCurrentProduct({
                                                ...currentProduct,
                                                productImageFile: file, // 圖片檔案
                                            });
                                        } else {
                                            alert("請上傳 JPG 或 PNG 格式的圖片");
                                            e.target.value = ""; // 清空輸入
                                        }
                                    }
                                }
                                }
                            />
                            {currentProduct.productImageUrl && (
                                <img
                                    src={currentProduct.productImageUrl}
                                    alt="product"
                                    width="100%"
                                    className="mt-2"
                                />
                            )}
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
                        onClick={isEditing ? updateProducts : createProducts}
                    >
                        {isEditing ? "儲存修改" : "新增"}
                    </Button>
                </Modal.Footer>
            </Modal>
        </Container>
    );
}
