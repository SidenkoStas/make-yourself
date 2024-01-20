FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir -p /make-yourself
RUN mkdir -p /make-yourself/static
RUN mkdir -p /make-yourself/media
