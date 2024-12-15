import React from 'react';
import { Row } from 'react-bootstrap';
import ProductManagement from '@/app/backstage/components/Product_Management';
import ClientProvider from '@/app/components/Client_Provider';

const ProductManagementPage = () => {
    return (
        <ClientProvider>
            <Row>
                <ProductManagement />
            </Row>
        </ClientProvider>
    );
};

export default ProductManagementPage;
