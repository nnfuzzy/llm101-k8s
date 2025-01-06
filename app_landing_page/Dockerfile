FROM nginx:latest

COPY ./html /usr/share/nginx/html
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
