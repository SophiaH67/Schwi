FROM node:16 as builder
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
RUN ./node_modules/.bin/tsc

FROM node:16 as runner
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm ci
COPY --from=builder /app/dist .
CMD ["node", "index.js"]