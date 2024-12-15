// src/components/Loader.js
"use client";  // 設定為客戶端組件

import React from 'react';
import { Spinner } from 'react-bootstrap';
import { useSelector } from 'react-redux';

const Loader = () => {
  const isLoading = useSelector((state) => state.loading.isLoading);

  if (!isLoading) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        zIndex: 9999,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Spinner animation="border" variant="light" />
    </div>
  );
};

export default Loader;
