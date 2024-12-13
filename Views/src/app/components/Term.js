"use client";

import React from "react";
import { useRouter } from "next/navigation"; // 引入 useRouter
import { Container, Row, Col, Spinner, Button } from "react-bootstrap";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示

const Term = ({ term }) => {
  const router = useRouter();

  if (!term) {
    return (
      <Container className="text-center my-4">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">正在加載...</p>
      </Container>
    );
  } else if (term.length === 0) {
    return (
      <Container className="text-center my-4">
        <p className="mt-2">查無此條文</p>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <Button variant="link" onClick={() => router.back()} className="mb-3">
        <FaArrowLeft />返回
      </Button>
      <Row xs={1} md={1} xl={1} xxl={1}>
        <Col>
          <div dangerouslySetInnerHTML={{ __html: term.content }}></div>
        </Col>
      </Row>
    </Container>
  );
}

export default Term;