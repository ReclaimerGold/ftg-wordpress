# WordPress with Redis Docker Image

This repository contains a custom Docker image based on the official WordPress 6.8.2-php8.4-apache image with Redis PHP modules pre-installed.

## Features

- **Base Image**: `wordpress:6.8.2-php8.4-apache`
- **Redis Support**: PHP Redis extension for caching and session management
- **Optimized**: Includes OPcache configuration for better performance
- **Multi-platform**: Built for both AMD64 and ARM64 architectures

## Quick Start

### Using Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  wordpress:
    image: ghcr.io/reclaimergold/ftg-wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress_data:/var/www/html
    depends_on:
      - db
      - redis

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: somewordpress
    volumes:
      - db_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  wordpress_data:
  db_data:
  redis_data:
```

### Using Docker Run

```bash
# Start Redis
docker run -d --name redis redis:7-alpine

# Start MySQL
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=somewordpress \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wordpress \
  -e MYSQL_PASSWORD=wordpress \
  mysql:8.0

# Start WordPress with Redis
docker run -d --name wordpress \
  --link mysql:mysql \
  --link redis:redis \
  -p 8080:80 \
  -e WORDPRESS_DB_HOST=mysql \
  -e WORDPRESS_DB_USER=wordpress \
  -e WORDPRESS_DB_PASSWORD=wordpress \
  -e WORDPRESS_DB_NAME=wordpress \
  ghcr.io/ReclaimerGold/ftg-wordpress:latest
```

## Building Locally

```bash
# Clone this repository
git clone https://github.com/reclaimergold/ftg-wordpress.git
cd ftg-wordpress

# Build the image
docker build -t ftg-wordpress:local .

# Run locally built image
docker run -d -p 8080:80 ftg-wordpress:local
```

## Redis Configuration in WordPress

To use Redis with WordPress, you'll need to install a Redis caching plugin or configure WordPress to use Redis for object caching. Here are some options:

### Option 1: Redis Object Cache Plugin

1. Install the "Redis Object Cache" plugin from the WordPress admin
2. Add the following to your `wp-config.php`:

```php
define('WP_REDIS_HOST', 'redis');
define('WP_REDIS_PORT', 6379);
define('WP_REDIS_DATABASE', 0);
```

### Option 2: Manual Object Cache Configuration

Add an `object-cache.php` file to your `wp-content` directory or use a Redis caching plugin.

## Environment Variables

The image supports all standard WordPress environment variables:

- `WORDPRESS_DB_HOST` - Database hostname
- `WORDPRESS_DB_USER` - Database username  
- `WORDPRESS_DB_PASSWORD` - Database password
- `WORDPRESS_DB_NAME` - Database name
- `WORDPRESS_TABLE_PREFIX` - Database table prefix (default: wp_)

## GitHub Actions Workflow

This repository includes a GitHub Actions workflow that automatically:

1. Builds the Docker image when a version tag is created (e.g., `v1.0.0`)
2. Publishes to GitHub Container Registry (ghcr.io)
3. Creates multi-platform builds (AMD64 and ARM64)
4. Tags images with semantic versioning (e.g., `v1.0.0`, `1.0`, `1`, `latest`)

## Setup Instructions

1. **Fork or create this repository** on GitHub
2. **Enable GitHub Actions** in your repository settings
3. **Create a version tag** to trigger the first build:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

The workflow will automatically publish your image to `ghcr.io/ReclaimerGold/ftg-wordpress:latest` and version-specific tags.

## Installed PHP Extensions

- **Redis**: For Redis connectivity and caching
- **OPcache**: For PHP bytecode caching and performance
- All standard WordPress extensions from the base image

## License

This project is licensed under the MIT License - see the LICENSE file for details.
