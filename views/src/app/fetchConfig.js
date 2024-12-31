const api_url = {
    production: "https://yielding-dove-samuelysliu-ce6a81f4.koyeb.app",
    uat: "https://classical-trish-samuelysliu-dbbd4671.koyeb.app",
    local: "http://localhost:8000"
  }
  
  const getConfig = (hostname) => {
    let env = "local";
    let gaId = "G-7362PCKYH6";
    let googleClientId = "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com";
  
    if (hostname === "shan-thai-website.vercel.app") {
      env = "uat";
      gaId = "G-7362PCKYH6";
      googleClientId = "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com";
    } else if (hostname === "www.shan-thai-team.com") {
      env = "production";
      gaId = "G-SE5TV10X0K";
      googleClientId = "979016396209-meutophgongc1r1kpskh6a5jq0l0gqc.apps.googleusercontent.com";
    }
  
    return {
      apiBaseUrl: api_url[env],
      gaId,
      googleClientId,
    };
  };

  export default getConfig;