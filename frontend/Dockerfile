FROM node:12

ENV TZ=America/Toronto

WORKDIR /database-frontend

COPY package.json ./
COPY yarn.lock ./

RUN yarn install 

COPY . .

# RUN npm run build

EXPOSE 3000

# CMD ["npm", "run", "deploy"]

CMD ["npm", "start"]