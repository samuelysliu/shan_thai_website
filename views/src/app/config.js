const api_url = {
  production: "https://yielding-dove-samuelysliu-ce6a81f4.koyeb.app",
  uat: "https://classical-trish-samuelysliu-dbbd4671.koyeb.app",
  local: "http://localhost:8000"
}

let hostname = "";
let gaId = "";
let googleClientId = "";

if (typeof window !== "undefined") {
  if (window.location.hostname === "shan-thai-website.vercel.app") {
    hostname = "uat";
    gaId = "G-7362PCKYH6";
    googleClientId = "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com";
  }

  else if (window.location.hostname === "www.shan-thai-team.com") {
    hostname = "production";
    gaId = "G-SE5TV10X0K";
    googleClientId = "979016396209-meutophgongc1r1rkp8kh6a5jq0l0gqc.apps.googleusercontent.com";
  }

  else {
    hostname = "local";
    gaId = "G-7362PCKYH6";
    googleClientId = "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com";
  }

}
else {
  hostname = "local";
  gaId = "G-7362PCKYH6";
  googleClientId = "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com";
}

const config = {
  apiBaseUrl: api_url[hostname],
  gaId: gaId,
  googleClientId: googleClientId
};

export default config;