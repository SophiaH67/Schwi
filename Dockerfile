FROM node:17 as builder
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
RUN npm run build

FROM node:17 as runner
WORKDIR /app
COPY --from=builder /app/dist .
COPY package.json .
COPY package-lock.json .
RUN npm ci
CMD ["npm", "start"]
