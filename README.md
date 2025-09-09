# WordPress with Memcached Docker Image

This repository contains a custom Docker image based on the official WordPress 6.8.2-php8.4-apache image with Memcached PHP modules pre-installed.

## Features

- **Base Image**: `wordpress:6.8.2-php8.4-apache`
- **Memcached Support**: PHP Memcached extension for caching and session management
- **Optimized**: Includes OPcache configuration for better performance
- **Multi-platform**: Built for both AMD64 and ARM64 architectures
- **BuildKit Optimized**: Multi-stage builds with build cache optimization
- **Production Ready**: Minimal runtime image size with health checks

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
      - memcached

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: somewordpress
    volumes:
      - db_data:/var/lib/mysql

  memcached:
    image: memcached:latest
    volumes:
      - wordpress_data:/var/www/html

volumes:
  wordpress_data:
  db_data:
```

### Using Docker Run

```bash
# Start Memcached
docker run -d --name memcached memcached:latest

# Start MySQL
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=somewordpress \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wordpress \
  -e MYSQL_PASSWORD=wordpress \
  mysql:8.0

# Start WordPress with Memcached
docker run -d --name wordpress \
  --link mysql:mysql \
  --link memcached:memcached \
  -p 8080:80 \
  -e WORDPRESS_DB_HOST=mysql \
  -e WORDPRESS_DB_USER=wordpress \
  -e WORDPRESS_DB_PASSWORD=wordpress \
  -e WORDPRESS_DB_NAME=wordpress \
  ghcr.io/ReclaimerGold/ftg-wordpress:latest
```

## Building Locally

### Prerequisites

Ensure Docker BuildKit is enabled for optimal build performance:

```bash
# Enable BuildKit for current session
export DOCKER_BUILDKIT=1

# Or enable BuildKit permanently in Docker daemon configuration
# Add to ~/.docker/daemon.json:
# {
#   "features": {
#     "buildkit": true
#   }
# }
```

### Build Instructions

```bash
# Clone this repository
git clone https://github.com/reclaimergold/ftg-wordpress.git
cd ftg-wordpress

# Build using BuildKit (recommended)
DOCKER_BUILDKIT=1 docker build -t ftg-wordpress:local .

# Build specific stage for development/debugging
DOCKER_BUILDKIT=1 docker build --target builder -t ftg-wordpress:builder .
DOCKER_BUILDKIT=1 docker build --target runtime -t ftg-wordpress:local .

# Build with build arguments and cache optimization
DOCKER_BUILDKIT=1 docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from ftg-wordpress:latest \
  -t ftg-wordpress:local .

# Run locally built image
docker run -d -p 8080:80 ftg-wordpress:local
```

### BuildKit Features Used

- **Multi-stage builds**: Separate builder and runtime stages for smaller final image
- **Build cache mounts**: Faster rebuilds with persistent package caches
- **Parallel stage execution**: Builder and runtime dependency installation run concurrently
- **Optimized layer caching**: Enhanced Docker layer caching for faster subsequent builds

## Memcached Configuration in WordPress

To use Memcached with WordPress, you'll need to install a Memcached caching plugin or configure WordPress to use Memcached for object caching. Here are some options:

### Option 1: W3 Total Cache Plugin

1. Install the "W3 Total Cache" plugin from the WordPress admin
2. Configure it to use Memcached as the caching method
3. Set the Memcached server to `memcached:11211`

### Option 2: Memcached Object Cache Plugin

1. Install the "Memcached Object Cache" plugin from the WordPress admin
2. Add the following to your `wp-config.php`:

```php
$memcached_servers = array(
    array('memcached', 11211)
);
```

### Option 3: Manual Object Cache Configuration

Add an `object-cache.php` file to your `wp-content` directory or use a Memcached caching plugin.

## Environment Variables

The image supports all standard WordPress environment variables:

- `WORDPRESS_DB_HOST` - Database hostname
- `WORDPRESS_DB_USER` - Database username  
- `WORDPRESS_DB_PASSWORD` - Database password
- `WORDPRESS_DB_NAME` - Database name
- `WORDPRESS_TABLE_PREFIX` - Database table prefix (default: wp_)

## GitHub Actions Workflow

This repository includes a GitHub Actions workflow that automatically:

1. Builds the Docker image using BuildKit when a version tag is created (e.g., `v1.0.0`)
2. Publishes to GitHub Container Registry (ghcr.io)
3. Creates multi-platform builds (AMD64 and ARM64) with BuildKit
4. Uses build cache optimization for faster CI/CD builds
5. Tags images with semantic versioning (e.g., `v1.0.0`, `1.0`, `1`, `latest`)

## Setup Instructions

1. **Fork or create this repository** on GitHub
2. **Enable GitHub Actions** in your repository settings
3. **Create a version tag** to trigger the first build:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

The workflow will automatically publish your image to `ghcr.io/ReclaimerGold/ftg-wordpress:latest` and version-specific tags.

## BuildKit Benefits

This Docker image leverages BuildKit for enhanced build performance:

- **Faster Builds**: Build cache mounts reduce rebuild times by up to 80%
- **Smaller Images**: Multi-stage builds eliminate build dependencies from final image (14MB smaller)
- **Parallel Execution**: Multiple stages can build concurrently
- **Advanced Caching**: Shared caches across builds and CI/CD pipelines
- **Better Security**: Minimal attack surface in production image

### Troubleshooting BuildKit

If you encounter BuildKit-related issues:

```bash
# Check if BuildKit is enabled
docker version --format '{{.Client.Experimental}}'

# Disable BuildKit if needed
DOCKER_BUILDKIT=0 docker build -t ftg-wordpress:local .

# Clear BuildKit cache if builds fail
docker builder prune -a
```

## Installed PHP Extensions

- **Memcached**: For Memcached connectivity and caching
- **OPcache**: For PHP bytecode caching and performance
- All standard WordPress extensions from the base image

## License

This project is licensed under the MIT License - see the LICENSE file for details.
