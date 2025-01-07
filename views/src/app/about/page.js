import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import NavBar from "@/app/components/Navbar";
import ClientProvider from "@/app/components/Client_Provider";
import { FaArrowLeft } from "react-icons/fa"; // 引入返回圖示
import Head from "next/head";
import Footer from "@/app/components/Footer";

const aboutPage = () => {
    return (
        <>
            {/* SEO 信息放在這裡 */}
            <Head>
                <title>善泰團隊 - 關於善泰團隊</title>
                <meta name="description" content="「善泰團隊」承襲著泰國佛教文化的智慧，致力於提供來自泰國的珍貴佛牌，帶來平安、祝福與庇佑。秉持著“善”與“泰”相互融合的精神，我們不僅販售佛牌，更傳遞心靈的平和與正能量。我們相信每一個佛牌背後，都有著深厚的信仰與力量，幫助每位顧客找到屬於自己的庇佑與安寧。加入「善泰團隊」，與我們一起守護自己與他人的幸福，讓善念與平和隨時相伴。" />
                <meta name="keywords" content="求財、改運、法事、佛牌、四面佛、佛教聖物、南傳聖物" />
            </Head>
            <ClientProvider>
                <NavBar />
                <Container>
                    <Container>
                        <Row xs={1} md={1} xl={1} xxl={1}>
                            <p></p>
                        </Row>
                        <Row xs={1} md={1} xl={1} xxl={1}>
                            <Col>
                                <h1>關於善泰團隊</h1>
                            </Col>
                        </Row>
                        <Row xs={1} md={1} xl={1} xxl={1}>
                            <Col>
                                <p>「善泰團隊」承襲著泰國佛教文化的智慧，致力於提供來自泰國的珍貴佛牌，帶來平安、祝福與庇佑。秉持著“善”與“泰”相互融合的精神，我們不僅販售佛牌，更傳遞心靈的平和與正能量。我們相信每一個佛牌背後，都有著深厚的信仰與力量，幫助每位顧客找到屬於自己的庇佑與安寧。加入「善泰團隊」，與我們一起守護自己與他人的幸福，讓善念與平和隨時相伴。</p>
                            </Col>
                        </Row>
                    </Container>
                </Container>
                <Footer />
            </ClientProvider>
        </>

    );
};

export default aboutPage;



