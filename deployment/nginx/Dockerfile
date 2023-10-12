FROM nginx

RUN mkdir -p /app

WORKDIR /app

RUN rm /etc/nginx/conf.d/default.conf
COPY deployment/nginx/nginx.conf /etc/nginx/conf.d
RUN mkdir -p /app/static && mkdir -p /app/media && mkdir -p /var/log/nginx

EXPOSE 8802
