# Build stage: generate the static site with Hugo
FROM klakegg/hugo:0.124.0-alpine AS builder
WORKDIR /src

# Install dependencies and build the site
COPY . .
RUN hugo --gc --minify

# Runtime stage: serve the static assets with Nginx
FROM nginx:1.27-alpine

# Copy the generated site from the builder stage
COPY --from=builder /src/public /usr/share/nginx/html

# Expose the default Nginx port
EXPOSE 80

# Use the default Nginx entrypoint/cmd
