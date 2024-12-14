# 使用 Node.js 作為基礎鏡像
FROM node:18-alpine

# 設置工作目錄
WORKDIR /app

# 複製依賴文件
COPY package.json package-lock.json ./

# 安裝生產依賴
RUN npm install --production

# 複製應用程式代碼到容器
COPY . .

# 構建 Next.js 應用
RUN npm run build

# 移除開發依賴（減小鏡像大小）
RUN npm prune --production

# 暴露應用埠
EXPOSE 3000

# 運行應用
CMD ["npm", "start"]
