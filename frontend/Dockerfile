FROM node:latest as node
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build --prod

FROM httpd:latest
COPY --from=node /app/dist/frontend /usr/local/apache2/htdocs
