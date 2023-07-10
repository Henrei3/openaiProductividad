FROM node:latest as node
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install @angular/cli


COPY . .

EXPOSE 4200
CMD ["ng","serve","--host","0.0.0.0"]
