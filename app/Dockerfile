# syntax=docker/dockerfile:1
FROM node:18-alpine
RUN apk --no-cache add curl
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "run", "dev"]
EXPOSE 5173
