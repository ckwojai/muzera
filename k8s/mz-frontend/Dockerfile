FROM node:14-alpine AS builder
WORKDIR /app
COPY app/package.json ./
RUN npm install
COPY ./app .
RUN npm run build

FROM nginx:1.19-alpine AS server
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder ./app/build /usr/share/nginx/html
