const api_url = {
  production: "",
  uat: "https://miserable-alina-samuelysliu-96038ede.koyeb.app",
  local: "http://localhost:8000"
}

const config = {
  apiBaseUrl: api_url[process.env.APP_ENV],
  };
  
  export default config;