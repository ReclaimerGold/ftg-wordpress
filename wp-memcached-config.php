<?php
/**
 * Memcached configuration for WordPress
 * 
 * Add these lines to your wp-config.php file to enable Memcached caching
 */

// Memcached Object Cache Configuration
define('WP_CACHE_KEY_SALT', getenv('WP_CACHE_KEY_SALT') ?: 'wp_');

// Memcached servers configuration
$memcached_servers = array(
    array(
        getenv('MEMCACHED_HOST') ?: 'memcached',
        intval(getenv('MEMCACHED_PORT') ?: 11211)
    )
);

// Optional: Enable Memcached for sessions
// ini_set('session.save_handler', 'memcached');
// ini_set('session.save_path', getenv('MEMCACHED_HOST') ?: 'memcached:11211');

// Enable WordPress object caching
define('WP_CACHE', true);

// Optional: Debug Memcached connections
// define('WP_DEBUG', true);
// define('WP_DEBUG_LOG', true);
?>
