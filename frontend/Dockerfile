FROM node:24-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN --mount=type=secret,id=proxy_ca,target=/tmp/proxy-ca.pem,required=false \
    if [ -f /tmp/proxy-ca.pem ]; then NODE_EXTRA_CA_CERTS=/tmp/proxy-ca.pem npm ci; else npm ci; fi
COPY . .
RUN npm run build
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
RUN chmod -R a+rX /usr/share/nginx/html
EXPOSE 80
