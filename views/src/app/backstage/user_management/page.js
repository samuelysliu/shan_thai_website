import React from 'react';
import { Row } from 'react-bootstrap';
import UserManagement from '../components/User_Management';
import ClientProvider from '@/app/components/Client_Provider';

const UserManagementPage = () => {
    return (
        <ClientProvider>
            <Row>
                <UserManagement />
            </Row>
        </ClientProvider>
    );
};

export default UserManagementPage;
