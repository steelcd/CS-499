FROM node:26.5.0-bookworm

WORKDIR /usr/src/app
COPY ./src/package*.json ./
RUN npm ci
COPY ./src/ .

WORKDIR /usr/src/app/app-admin
RUN npm ci
RUN npm run build

WORKDIR /usr/src/app

USER node

CMD ["npm", "start"]