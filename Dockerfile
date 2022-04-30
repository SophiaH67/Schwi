FROM node:17 as runner
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
CMD ["npm", "start"]
