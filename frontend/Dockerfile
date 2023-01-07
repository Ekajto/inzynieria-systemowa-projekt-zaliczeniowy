###################
# BUILD
###################

FROM node:18-alpine As build

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm ci --silent
COPY . ./
RUN npm run build

###################
# EXPOSE
###################

FROM nginx:stable-alpine
EXPOSE 80

COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

CMD ["nginx", "-c", "/etc/nginx/nginx.conf", "-g", "daemon off;"]