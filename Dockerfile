FROM node:20-alpine
workdir /app
COPY package*.json ./
RUN npm install --production

COPY . .
EXPOSE 8080
USER node 
CMD ["npm", "start"]

