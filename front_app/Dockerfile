FROM node:alpine
WORKDIR /app
COPY package.json ./       
COPY package-lock.json ./
COPY ./ ./
RUN npm init
# CMD ["npm","init"]
CMD ["npm","run","start"]
CMD ["npx","create-react-app","mon-app"]