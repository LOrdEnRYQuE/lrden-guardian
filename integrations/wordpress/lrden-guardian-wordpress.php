<?php
/**
 * Plugin Name: LRDEnE Guardian - AI Safety for WordPress
 * Plugin URI: https://github.com/LOrdEnRYQuE/lrden-guardian
 * Description: Real-time AI safety and hallucination detection for WordPress content
 * Version: 1.0.0
 * Author: LRDEnE Technology Team
 * Author URI: https://lrden.com
 * License: Proprietary
 * Text Domain: lrden-guardian
 * Domain Path: /languages
 * Network: true
 * Requires at least: 5.8
 * Requires PHP: 7.4
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('LRDEN_GUARDIAN_VERSION', '1.0.0');
define('LRDEN_GUARDIAN_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('LRDEN_GUARDIAN_PLUGIN_URL', plugin_dir_url(__FILE__));
define('LRDEN_GUARDIAN_API_ENDPOINT', get_option('lrden_guardian_api_endpoint', 'http://localhost:5001'));

/**
 * Main LRDEnE Guardian WordPress Plugin Class
 */
class LRDEnEGuardianWordPress {
    
    private $api_endpoint;
    private $settings;
    
    public function __construct() {
        $this->api_endpoint = LRDEN_GUARDIAN_API_ENDPOINT;
        $this->settings = get_option('lrden_guardian_settings', []);
        
        $this->init_hooks();
    }
    
    /**
     * Initialize WordPress hooks
     */
    private function init_hooks() {
        // Admin hooks
        add_action('admin_menu', [$this, 'add_admin_menu']);
        add_action('admin_init', [$this, 'register_settings']);
        add_action('admin_enqueue_scripts', [$this, 'enqueue_admin_scripts']);
        
        // Content analysis hooks
        add_action('save_post', [$this, 'analyze_post_on_save'], 10, 3);
        add_action('wp_insert_comment', [$this, 'analyze_comment'], 10, 3);
        add_action('add_meta_boxes', [$this, 'add_post_meta_box']);
        add_action('wp_ajax_lrden_guardian_analyze', [$this, 'ajax_analyze_content']);
        
        // Editor integration
        add_filter('content_save_pre', [$this, 'analyze_content_before_save']);
        add_filter('title_save_pre', [$this, 'analyze_title_before_save']);
        
        // Frontend protection
        add_action('wp_enqueue_scripts', [$this, 'enqueue_frontend_scripts']);
        add_filter('the_content', [$this, 'add_content_badges']);
        add_filter('comment_text', [$this, 'add_comment_badges']);
        
        // REST API integration
        add_action('rest_api_init', [$this, 'register_rest_routes']);
    }
    
    /**
     * Add admin menu items
     */
    public function add_admin_menu() {
        add_menu_page(
            'LRDEnE Guardian',
            'LRDEnE Guardian',
            'manage_options',
            'lrden-guardian',
            [$this, 'admin_dashboard_page'],
            'dashicons-shield',
            30
        );
        
        add_submenu_page(
            'lrden-guardian',
            'Dashboard',
            'Dashboard',
            'manage_options',
            'lrden-guardian',
            [$this, 'admin_dashboard_page']
        );
        
        add_submenu_page(
            'lrden-guardian',
            'Settings',
            'Settings',
            'manage_options',
            'lrden-guardian-settings',
            [$this, 'admin_settings_page']
        );
        
        add_submenu_page(
            'lrden-guardian',
            'Analytics',
            'Analytics',
            'manage_options',
            'lrden-guardian-analytics',
            [$this, 'admin_analytics_page']
        );
    }
    
    /**
     * Register plugin settings
     */
    public function register_settings() {
        register_setting('lrden_guardian_settings', 'lrden_guardian_api_endpoint');
        register_setting('lrden_guardian_settings', 'lrden_guardian_settings');
        
        add_settings_section(
            'lrden_guardian_general',
            'General Settings',
            [$this, 'settings_section_callback'],
            'lrden-guardian-settings'
        );
        
        add_settings_field(
            'api_endpoint',
            'API Endpoint',
            [$this, 'api_endpoint_field_callback'],
            'lrden-guardian-settings',
            'lrden_guardian_general'
        );
        
        add_settings_field(
            'auto_analyze_posts',
            'Auto-Analyze Posts',
            [$this, 'checkbox_field_callback'],
            'lrden-guardian-settings',
            'lrden_guardian_general',
            ['name' => 'auto_analyze_posts', 'description' => 'Automatically analyze posts on save']
        );
        
        add_settings_field(
            'auto_analyze_comments',
            'Auto-Analyze Comments',
            [$this, 'checkbox_field_callback'],
            'lrden-guardian-settings',
            'lrden_guardian_general',
            ['name' => 'auto_analyze_comments', 'description' => 'Automatically analyze comments before posting']
        );
        
        add_settings_field(
            'show_badges',
            'Show Safety Badges',
            [$this, 'checkbox_field_callback'],
            'lrden-guardian-settings',
            'lrden_guardian_general',
            ['name' => 'show_badges', 'description' => 'Display safety badges on content']
        );
    }
    
    /**
     * Enqueue admin scripts and styles
     */
    public function enqueue_admin_scripts($hook) {
        if (strpos($hook, 'lrden-guardian') !== false) {
            wp_enqueue_style('lrden-guardian-admin', LRDEN_GUARDIAN_PLUGIN_URL . 'assets/admin.css', [], LRDEN_GUARDIAN_VERSION);
            wp_enqueue_script('lrden-guardian-admin', LRDEN_GUARDIAN_PLUGIN_URL . 'assets/admin.js', ['jquery'], LRDEN_GUARDIAN_VERSION, true);
            
            wp_localize_script('lrden-guardian-admin', 'lrden_guardian', [
                'api_endpoint' => $this->api_endpoint,
                'nonce' => wp_create_nonce('lrden_guardian_nonce'),
                'strings' => [
                    'analyzing' => 'Analyzing with LRDEnE Guardian...',
                    'error' => 'Analysis failed. Please check your connection.',
                    'safe' => 'Content is safe',
                    'warning' => 'Content requires review'
                ]
            ]);
        }
        
        // Load on post edit pages
        if (in_array($hook, ['post.php', 'post-new.php'])) {
            wp_enqueue_script('lrden-guardian-editor', LRDEN_GUARDIAN_PLUGIN_URL . 'assets/editor.js', ['jquery'], LRDEN_GUARDIAN_VERSION, true);
        }
    }
    
    /**
     * Enqueue frontend scripts
     */
    public function enqueue_frontend_scripts() {
        if ($this->get_setting('show_badges', true)) {
            wp_enqueue_style('lrden-guardian-frontend', LRDEN_GUARDIAN_PLUGIN_URL . 'assets/frontend.css', [], LRDEN_GUARDIAN_VERSION);
            wp_enqueue_script('lrden-guardian-frontend', LRDEN_GUARDIAN_PLUGIN_URL . 'assets/frontend.js', [], LRDEN_GUARDIAN_VERSION, true);
        }
    }
    
    /**
     * Add meta box to post editor
     */
    public function add_post_meta_box() {
        add_meta_box(
            'lrden-guardian-analysis',
            'LRDEnE Guardian Analysis',
            [$this, 'post_meta_box_callback'],
            ['post', 'page'],
            'side',
            'high'
        );
    }
    
    /**
     * Post meta box callback
     */
    public function post_meta_box_callback($post) {
        $analysis = get_post_meta($post->ID, '_lrden_guardian_analysis', true);
        $guardian_score = get_post_meta($post->ID, '_lrden_guardian_score', true);
        $is_safe = get_post_meta($post->ID, '_lrden_guardian_safe', true);
        
        echo '<div id="lrden-guardian-meta-box">';
        
        if ($analysis) {
            $status_class = $is_safe ? 'safe' : 'warning';
            $status_icon = $is_safe ? '✅' : '⚠️';
            $status_text = $is_safe ? 'Safe Content' : 'Requires Review';
            
            echo "<div class='lrden-status {$status_class}'>";
            echo "<span class='lrden-icon'>{$status_icon}</span>";
            echo "<span class='lrden-text'>{$status_text}</span>";
            echo "</div>";
            
            echo "<div class='lrden-metrics'>";
            echo "<div class='lrden-metric'>";
            echo "<span class='lrden-label'>Guardian Score:</span>";
            echo "<span class='lrden-value'>" . number_format($guardian_score, 3) . "</span>";
            echo "</div>";
            echo "</div>";
            
            echo "<button type='button' id='lrden-reanalyze' class='button button-secondary'>Re-analyze</button>";
        } else {
            echo "<p>No analysis available.</p>";
            echo "<button type='button' id='lrden-analyze-now' class='button button-primary'>Analyze Now</button>";
        }
        
        echo '</div>';
    }
    
    /**
     * Analyze post on save
     */
    public function analyze_post_on_save($post_id, $post, $update) {
        if (!$this->get_setting('auto_analyze_posts', true)) {
            return;
        }
        
        if (wp_is_post_revision($post_id) || $post->post_status === 'auto-draft') {
            return;
        }
        
        $content = $post->post_content . ' ' . $post->post_title;
        $this->analyze_content($content, $post_id, 'post');
    }
    
    /**
     * Analyze comment
     */
    public function analyze_comment($comment_id, $comment_approved, $comment_data) {
        if (!$this->get_setting('auto_analyze_comments', true)) {
            return;
        }
        
        $content = $comment_data->comment_content;
        $this->analyze_content($content, $comment_id, 'comment');
    }
    
    /**
     * Analyze content
     */
    private function analyze_content($content, $id, $type) {
        $response = wp_remote_post($this->api_endpoint . '/analyze', [
            'body' => json_encode([
                'content' => $content,
                'context' => [
                    'source' => 'wordpress_plugin',
                    'type' => $type,
                    'url' => get_site_url(),
                    'timestamp' => current_time('mysql')
                ]
            ]),
            'headers' => [
                'Content-Type' => 'application/json',
            ],
            'timeout' => 10,
        ]);
        
        if (is_wp_error($response)) {
            error_log('LRDEnE Guardian API Error: ' . $response->get_error_message());
            return false;
        }
        
        $body = wp_remote_retrieve_body($response);
        $result = json_decode($body, true);
        
        if ($result && isset($result['guardian_score'])) {
            $this->save_analysis_result($id, $type, $result);
            return $result;
        }
        
        return false;
    }
    
    /**
     * Save analysis result
     */
    private function save_analysis_result($id, $type, $result) {
        if ($type === 'post') {
            update_post_meta($id, '_lrden_guardian_analysis', $result);
            update_post_meta($id, '_lrden_guardian_score', $result['guardian_score']);
            update_post_meta($id, '_lrden_guardian_safe', $result['is_safe']);
            update_post_meta($id, '_lrden_guardian_risk_level', $result['risk_level']);
            update_post_meta($id, '_lrden_guardian_analyzed_at', current_time('mysql'));
        } elseif ($type === 'comment') {
            update_comment_meta($id, '_lrden_guardian_analysis', $result);
            update_comment_meta($id, '_lrden_guardian_score', $result['guardian_score']);
            update_comment_meta($id, '_lrden_guardian_safe', $result['is_safe']);
            update_comment_meta($id, '_lrden_guardian_risk_level', $result['risk_level']);
            update_comment_meta($id, '_lrden_guardian_analyzed_at', current_time('mysql'));
        }
    }
    
    /**
     * AJAX analyze content
     */
    public function ajax_analyze_content() {
        check_ajax_referer('lrden_guardian_nonce', 'nonce');
        
        if (!current_user_can('edit_posts')) {
            wp_die('Unauthorized');
        }
        
        $content = sanitize_textarea_field($_POST['content']);
        $id = intval($_POST['id']);
        $type = sanitize_text_field($_POST['type']);
        
        $result = $this->analyze_content($content, $id, $type);
        
        if ($result) {
            wp_send_json_success($result);
        } else {
            wp_send_json_error('Analysis failed');
        }
    }
    
    /**
     * Add content badges
     */
    public function add_content_badges($content) {
        if (!$this->get_setting('show_badges', true)) {
            return $content;
        }
        
        global $post;
        
        if (!$post) {
            return $content;
        }
        
        $is_safe = get_post_meta($post->ID, '_lrden_guardian_safe', true);
        $guardian_score = get_post_meta($post->ID, '_lrden_guardian_score', true);
        
        if ($guardian_score === '') {
            return $content;
        }
        
        $badge_class = $is_safe ? 'lrden-safe' : 'lrden-warning';
        $badge_icon = $is_safe ? '✅' : '⚠️';
        $badge_text = $is_safe ? 'Safe' : 'Review';
        
        $badge = "<div class='lrden-guardian-badge {$badge_class}'>";
        $badge .= "<span class='lrden-icon'>{$badge_icon}</span>";
        $badge .= "<span class='lrden-text'>LRDEnE Guardian: {$badge_text}</span>";
        $badge .= "<span class='lrden-score'>Score: " . number_format($guardian_score, 3) . "</span>";
        $badge .= "</div>";
        
        return $badge . $content;
    }
    
    /**
     * Add comment badges
     */
    public function add_comment_badges($comment_text) {
        if (!$this->get_setting('show_badges', true)) {
            return $comment_text;
        }
        
        $comment = get_comment();
        
        if (!$comment) {
            return $comment_text;
        }
        
        $is_safe = get_comment_meta($comment->comment_ID, '_lrden_guardian_safe', true);
        $guardian_score = get_comment_meta($comment->comment_ID, '_lrden_guardian_score', true);
        
        if ($guardian_score === '') {
            return $comment_text;
        }
        
        $badge_class = $is_safe ? 'lrden-safe' : 'lrden-warning';
        $badge_icon = $is_safe ? '✅' : '⚠️';
        
        $badge = "<span class='lrden-guardian-comment-badge {$badge_class}'>";
        $badge .= "<span class='lrden-icon'>{$badge_icon}</span>";
        $badge .= "<span class='lrden-score'>" . number_format($guardian_score, 3) . "</span>";
        $badge .= "</span>";
        
        return $badge . ' ' . $comment_text;
    }
    
    /**
     * Register REST API routes
     */
    public function register_rest_routes() {
        register_rest_route('lrden-guardian/v1', '/analyze', [
            'methods' => 'POST',
            'callback' => [$this, 'rest_analyze_content'],
            'permission_callback' => [$this, 'rest_permissions_check'],
            'args' => [
                'content' => [
                    'required' => true,
                    'type' => 'string',
                    'sanitize_callback' => 'sanitize_textarea_field'
                ],
                'context' => [
                    'type' => 'object',
                    'sanitize_callback' => [$this, 'sanitize_context']
                ]
            ]
        ]);
    }
    
    /**
     * REST API analyze content callback
     */
    public function rest_analyze_content($request) {
        $content = $request->get_param('content');
        $context = $request->get_param('context');
        
        $result = $this->analyze_content($content, 0, 'api');
        
        if ($result) {
            return new WP_REST_Response($result, 200);
        } else {
            return new WP_Error('analysis_failed', 'Content analysis failed', ['status' => 500]);
        }
    }
    
    /**
     * REST API permissions check
     */
    public function rest_permissions_check() {
        return current_user_can('edit_posts');
    }
    
    /**
     * Get setting value
     */
    private function get_setting($key, $default = false) {
        return isset($this->settings[$key]) ? $this->settings[$key] : $default;
    }
    
    /**
     * Admin dashboard page
     */
    public function admin_dashboard_page() {
        include LRDEN_GUARDIAN_PLUGIN_DIR . 'templates/dashboard.php';
    }
    
    /**
     * Admin settings page
     */
    public function admin_settings_page() {
        include LRDEN_GUARDIAN_PLUGIN_DIR . 'templates/settings.php';
    }
    
    /**
     * Admin analytics page
     */
    public function admin_analytics_page() {
        include LRDEN_GUARDIAN_PLUGIN_DIR . 'templates/analytics.php';
    }
    
    /**
     * Settings callbacks
     */
    public function settings_section_callback() {
        echo '<p>Configure your LRDEnE Guardian integration settings.</p>';
    }
    
    public function api_endpoint_field_callback() {
        $value = get_option('lrden_guardian_api_endpoint', 'http://localhost:5001');
        echo "<input type='url' name='lrden_guardian_api_endpoint' value='" . esc_attr($value) . "' class='regular-text'>";
        echo "<p class='description'>URL of your LRDEnE Guardian API server</p>";
    }
    
    public function checkbox_field_callback($args) {
        $name = $args['name'];
        $value = isset($this->settings[$name]) ? $this->settings[$name] : false;
        echo "<input type='checkbox' name='lrden_guardian_settings[{$name}]' value='1' " . checked($value, 1, false) . ">";
        echo "<label class='description'>{$args['description']}</label>";
    }
}

// Initialize the plugin
new LRDEnEGuardianWordPress();
