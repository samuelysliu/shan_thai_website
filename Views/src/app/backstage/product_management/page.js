import React from 'react';
import { Row } from 'react-bootstrap';
import ProductManagement from '@/app/components/Product_Management';
import Sidebar from '@/app/components/Sidebar';

const ProductManagementPage = () => {
    return (
        <Row>
            <ProductManagement />
        </Row>
    );
};

export default ProductManagementPage;
