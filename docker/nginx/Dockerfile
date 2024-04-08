FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY proxy_params.txt /etc/nginx

# SSL certificates
COPY /etc/letsencrypt/live/tomilov.space/fullchain.pem /etc/nginx/certs/
COPY /etc/letsencrypt/live/tomilov.space/privkey.pem /etc/nginx/certs/
