import React from 'react';
import { Row } from 'react-bootstrap';
import ClientProvider from '@/app/components/Client_Provider';
import TermManagement from '@/app/backstage/components/Term_Management';

const TermManagementPage = () => {
    return (
        <ClientProvider>
            <Row>
                <TermManagement />
            </Row>
        </ClientProvider>
    );
};

export default TermManagementPage;
