const api_url = {
  production: "https://yielding-dove-samuelysliu-ce6a81f4.koyeb.app",
  uat: "https://classical-trish-samuelysliu-dbbd4671.koyeb.app",
  local: "http://localhost:8000"
}

const gaId = {
  production: "G-SE5TV10X0K",
  uat: "G-7362PCKYH6",
  local: "G-7362PCKYH6"
}

const googleClientId = {
  production: "979016396209-meutophgongc1r1kpskh6a5jq0l0gqc.apps.googleusercontent.com",
  uat: "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com",
  local: "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com"
}

const config = {
  apiBaseUrl: api_url[process.env.NEXT_PUBLIC_ENV],
  gaId: gaId[process.env.NEXT_PUBLIC_ENV],
  googleClientId: googleClientId[process.env.NEXT_PUBLIC_ENV]
};
console.log(process.env.NEXT_PUBLIC_ENV)
export default config;