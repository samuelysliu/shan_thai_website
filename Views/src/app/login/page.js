import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../redux/slices/userSlice';
import axios from 'axios';
import Head from 'next/head';

const LoginPage = () => {
    const dispatch = useDispatch();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/login', { email, password });
            if (response.data && response.data.detail === "Login successful") {
                dispatch(login(response.data.user_info)); // 假設API回傳用戶信息在 user_info 中
                alert('Login successful');
            }
        } catch (error) {
            alert('Login failed. Please try again.');
        }
    };

    return (
        <>
            <Head>
                <title>Login - My App</title>
                <meta name="description" content="User login page for My App" />
            </Head>
            <div>
                <h2>Login</h2>
                {/* 表單內容 */}
            </div>

            <div>
                <h2>Login</h2>
                <form onSubmit={handleLogin}>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                    />
                    <button type="submit">Login</button>
                </form>
            </div>
        </>
    );
};

export default LoginPage;
