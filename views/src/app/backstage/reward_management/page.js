import React from 'react';
import { Row } from 'react-bootstrap';
import ClientProvider from '@/app/components/Client_Provider';
import RewardManagement from '../components/Reward_Management';

const RewardManagementPage = () => {
    return (
        <ClientProvider>
            <Row>
                <RewardManagement />
            </Row>
        </ClientProvider>
    );
};

export default RewardManagementPage;
