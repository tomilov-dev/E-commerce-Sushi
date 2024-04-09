FROM nginx:latest

RUN mkdir -p /var/nginx/proxy_temp
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx
COPY proxy_params.txt /etc/nginx
