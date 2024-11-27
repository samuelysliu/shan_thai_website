"use client";

import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";

export default function AddTagModal({ show, handleClose, handleSave }) {
  const [newTag, setNewTag] = useState("");

  const handleInputChange = (e) => setNewTag(e.target.value);

  const handleSaveTag = () => {
    if (newTag.trim() === "") {
      alert("標籤名稱不可為空！");
      return;
    }
    handleSave(newTag);
    setNewTag("");
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>新增標籤</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form.Group className="mb-3">
          <Form.Label>標籤名稱</Form.Label>
          <Form.Control
            type="text"
            value={newTag}
            onChange={handleInputChange}
            placeholder="輸入新標籤名稱"
          />
        </Form.Group>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          取消
        </Button>
        <Button variant="primary" onClick={handleSaveTag}>
          儲存
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
