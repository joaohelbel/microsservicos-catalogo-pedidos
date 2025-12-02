FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json tsconfig.json vite.config.mts ./
COPY src ./src
COPY index.html ./
RUN npm install
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
