FROM node:16

WORKDIR /workplace

COPY ./frontend/package*.json /workplace/
RUN npm install

COPY ./frontend /workplace

RUN npm run build

CMD ["npm", "run", "dev"]