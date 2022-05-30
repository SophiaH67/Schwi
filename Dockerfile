FROM node:17 as builder
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
# Replace "class View" with "interface View" in node_modules/compromise/types/view/one.ts
RUN sed -i 's/class View/interface View/g' node_modules/compromise/types/view/one.ts
COPY . .
RUN npm run build

FROM node:17 as runner
WORKDIR /app
COPY --from=builder /app/dist .
COPY package.json .
COPY package-lock.json .
RUN npm ci
CMD ["npm", "start"]
