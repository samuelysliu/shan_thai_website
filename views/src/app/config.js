const api_url = {
  production: "",
  uat: "https://classical-trish-samuelysliu-dbbd4671.koyeb.app",
  local: "http://localhost:8000"
}

const config = {
  apiBaseUrl: api_url[process.env.NEXT_PUBLIC_APP_ENV],
  };
  
  export default config;