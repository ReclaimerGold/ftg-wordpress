# Use the official WordPress image with PHP 8.4 and Apache
FROM wordpress:6.8.2-php8.4-apache

# Install system dependencies for Redis
RUN apt-get update && apt-get install -y \
    libhiredis-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Redis PHP extension
RUN pecl install redis \
    && docker-php-ext-enable redis

# Verify Redis extension is installed
RUN php -m | grep redis

# Optional: Install additional useful PHP extensions for WordPress + Redis
RUN docker-php-ext-install opcache

# Set recommended PHP configuration for production
RUN { \
    echo 'opcache.memory_consumption=128'; \
    echo 'opcache.interned_strings_buffer=8'; \
    echo 'opcache.max_accelerated_files=4000'; \
    echo 'opcache.revalidate_freq=2'; \
    echo 'opcache.fast_shutdown=1'; \
    echo 'opcache.enable_cli=1'; \
} > /usr/local/etc/php/conf.d/opcache-recommended.ini

# Set Redis configuration
RUN { \
    echo 'redis.session.locking_enabled=1'; \
    echo 'redis.session.lock_expire=30'; \
    echo 'redis.session.lock_wait_time=50000'; \
} > /usr/local/etc/php/conf.d/redis.ini

# Expose port 80
EXPOSE 80

# Use the default WordPress entrypoint
CMD ["apache2-foreground"]
