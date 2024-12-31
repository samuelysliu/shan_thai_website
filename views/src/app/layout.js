import localFont from "next/font/local";
import "./globals.css";
import "./backstage.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import config from "./config";


const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

const gaId = config.gaId;

export const metadata = {
  title: "善泰團隊 - 南傳聖物請供",
  description: "想要求財、改運、佛牌、供尊，通通可以在這裡找到。善泰團隊，幫您找到最適合的聖物。",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <script async src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`} />
        <script>
          {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', '${gaId}');
          `}
        </script>
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable}`} >
        {children}
      </body>
    </html>
  );
}
