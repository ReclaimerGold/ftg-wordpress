# syntax=docker/dockerfile:1
# BuildKit multi-stage build for WordPress with Memcached

# Stage 1: Build stage for compiling extensions
FROM wordpress:6.8.2-php8.4-apache AS builder

# Install build dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    libmemcached-dev \
    libz-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Memcached PHP extension with build cache
RUN --mount=type=cache,target=/tmp/pear,sharing=locked \
    pecl install memcached

# Stage 2: Runtime stage - clean WordPress image
FROM wordpress:6.8.2-php8.4-apache AS runtime

# Install only runtime dependencies (no build tools)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    libmemcached11 \
    libz1 \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled extensions from builder stage
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/

# Enable Memcached extension
RUN docker-php-ext-enable memcached

# Install OPcache (built-in extension, no compilation needed)
RUN docker-php-ext-install opcache

# Verify Memcached extension is installed
RUN php -m | grep memcached

# Set recommended PHP configuration for production
RUN { \
    echo 'opcache.memory_consumption=128'; \
    echo 'opcache.interned_strings_buffer=8'; \
    echo 'opcache.max_accelerated_files=4000'; \
    echo 'opcache.revalidate_freq=2'; \
    echo 'opcache.fast_shutdown=1'; \
    echo 'opcache.enable_cli=1'; \
} > /usr/local/etc/php/conf.d/opcache-recommended.ini

# Set Memcached configuration
RUN { \
    echo 'memcached.sess_locking=1'; \
    echo 'memcached.sess_lock_wait_min=150'; \
    echo 'memcached.sess_lock_wait_max=150'; \
} > /usr/local/etc/php/conf.d/memcached.ini

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Expose port 80
EXPOSE 80

# Use the default WordPress entrypoint
CMD ["apache2-foreground"]
