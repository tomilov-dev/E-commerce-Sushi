FROM nginx:latest

RUN mkdir -p /var/nginx/proxy_temp
RUN rm /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/conf.d
COPY proxy_params.txt /etc/nginx
