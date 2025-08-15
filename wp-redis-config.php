<?php
/**
 * Redis configuration for WordPress
 * 
 * Add these lines to your wp-config.php file to enable Redis caching
 */

// Redis Object Cache Configuration
define('WP_REDIS_HOST', getenv('WP_REDIS_HOST') ?: 'redis');
define('WP_REDIS_PORT', getenv('WP_REDIS_PORT') ?: 6379);
define('WP_REDIS_DATABASE', getenv('WP_REDIS_DATABASE') ?: 0);
define('WP_REDIS_TIMEOUT', 1);
define('WP_REDIS_READ_TIMEOUT', 1);

// Optional: Redis authentication (if your Redis instance requires a password)
// define('WP_REDIS_PASSWORD', getenv('WP_REDIS_PASSWORD'));

// Optional: Redis prefix for cache keys
define('WP_REDIS_PREFIX', getenv('WP_REDIS_PREFIX') ?: 'wp');

// Optional: Enable Redis for sessions
// define('WP_REDIS_DISABLE_BANNERS', true);

// Enable Redis object caching
define('WP_CACHE', true);

// Optional: Debug Redis connections
// define('WP_DEBUG', true);
// define('WP_DEBUG_LOG', true);
?>
