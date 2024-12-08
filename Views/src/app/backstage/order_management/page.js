import React from 'react';
import { Row } from 'react-bootstrap';
import OrderManagement from '../components/Order_Management';
import ClientProvider from '@/app/components/Client_Provider';

const OrderManagementPage = () => {
    return (
        <ClientProvider>
            <Row>
                <OrderManagement />
            </Row>
        </ClientProvider>
    );
};

export default OrderManagementPage;
