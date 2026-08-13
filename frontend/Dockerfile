# --- Stage 1: build ---
# Node is only needed to COMPILE the React app into static HTML/JS/CSS.
# It is NOT needed to actually serve those files afterward.
FROM node:20-slim AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# --- Stage 2: serve ---
# A fresh, tiny nginx image -- none of Node, npm, or any dev dependency
# is present here. Only the final built static files get copied over
# from the "build" stage above. This is the actual point of a
# multi-stage build: the final shipped image is a lightweight static
# file server, not a full Node.js environment nobody needs at runtime.
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
