# 使用 Node.js 官方 LTS 版本作為基礎映像
FROM node:18-alpine AS builder

# 添加系統依賴
RUN apk add --no-cache python3 make g++ bash

# 設置工作目錄
WORKDIR /app

# 複製 package.json 和 yarn.lock
COPY package.json yarn.lock ./

# 安裝依賴
RUN yarn install --frozen-lockfile

# 複製應用代碼
COPY . .

# 構建 Next.js 應用
RUN yarn build

# -----
# 生產環境
# -----
FROM node:18-alpine AS runner

# 設置工作目錄
WORKDIR /app

ENV NEXT_PUBLIC_APP_ENV=
ENV NEXT_PUBLIC_GA_ID=
ENV NEXT_PUBLIC_GOOGLE_CLIENT_ID=


# 複製必要的文件和構建結果
COPY package.json yarn.lock ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/next.config.mjs ./
COPY --from=builder /app/node_modules ./node_modules

# 安裝僅生產依賴項
RUN yarn install --production --frozen-lockfile

# 暴露端口
EXPOSE 3000

# 啟動應用
CMD ["yarn", "start"]