# 🔌 LRDEnE Guardian Integration Plugins

Extend LRDEnE Guardian's AI safety protection to the platforms you use every day.

## 📦 Available Integrations

### 🌐 WordPress Plugin
**File**: `wordpress/lrden-guardian-wordpress.php`

**Features:**
- Real-time post and comment analysis
- Automatic content validation on save
- Safety badges on published content
- Admin dashboard with analytics
- REST API endpoints for custom integrations
- Settings panel for configuration

**Installation:**
1. Copy `lrden-guardian-wordpress.php` to `/wp-content/plugins/`
2. Activate in WordPress admin
3. Configure API endpoint in settings
4. Enable auto-analysis features

**Usage:**
- Posts are automatically analyzed on save
- Comments are checked before posting
- Manual analysis via admin panel
- Safety badges displayed on content

---

### 💬 Slack Integration
**File**: `slack/lrden-guardian-slack.py`

**Features:**
- Real-time message analysis
- Risk alerts via DM
- Manual analysis commands
- Status checking commands
- Analysis caching for performance
- Configurable alert thresholds

**Installation:**
```bash
# Install dependencies
pip install slack-bolt requests

# Set environment variables
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
export LRDEN_GUARDIAN_API_ENDPOINT="http://localhost:5001"

# Run the bot
python slack/lrden-guardian-slack.py
```

**Commands:**
- `/guardian-analyze <text>` - Manual analysis
- `/guardian-status` - Check API status
- `/guardian-settings` - View configuration

**Usage:**
- Messages are automatically analyzed
- Risk alerts sent via DM
- Use commands for manual checks

---

### 🎮 Discord Integration
**File**: `discord/lrden-guardian-discord.py`

**Features:**
- Real-time message monitoring
- Risk alerts via DM or channel
- Rich embed analysis results
- Command-based interface
- Server statistics tracking
- Customizable alert levels

**Installation:**
```bash
# Install dependencies
pip install discord.py requests

# Set environment variables
export DISCORD_BOT_TOKEN="your-bot-token"
export LRDEN_GUARDIAN_API_ENDPOINT="http://localhost:5001"

# Run the bot
python discord/lrden-guardian-discord.py
```

**Commands:**
- `/guardian analyze <text>` - Manual analysis
- `/guardian status` - Check API status
- `/guardian settings` - View configuration
- `/guardian help` - Show help

**Usage:**
- Automatic message analysis
- Risk alerts for problematic content
- Rich embed analysis reports

---

## 🚀 Quick Start Guide

### 1. Set Up LRDEnE Guardian API
First, ensure your LRDEnE Guardian web dashboard is running:
```bash
cd web_dashboard
python app.py
```

### 2. Choose Your Integration
Select the platform you want to integrate with and follow the specific installation instructions.

### 3. Configure API Connection
All integrations need to connect to your LRDEnE Guardian API:
- **Default endpoint**: `http://localhost:5001`
- **API path**: `/analyze` for content analysis
- **Health check**: `/api-info` for status verification

### 4. Test the Integration
Use the built-in test commands to verify everything is working:
- WordPress: Check admin dashboard
- Slack: Use `/guardian-status` command
- Discord: Use `/guardian status` command

## 🔧 Configuration Options

### Common Settings
All integrations support these configuration options:

- **API Endpoint**: URL of LRDEnE Guardian server
- **Auto-Analysis**: Enable/disable automatic content checking
- **Risk Thresholds**: Configure when to trigger alerts
- **Notification Settings**: Control how alerts are sent
- **Cache Settings**: Configure analysis result caching

### Platform-Specific Settings

#### WordPress
- **Post Analysis**: Analyze posts on save
- **Comment Analysis**: Check comments before posting
- **Badge Display**: Show safety badges on content
- **User Roles**: Configure who can see analysis results

#### Slack
- **Channel Monitoring**: Select channels to monitor
- **Alert Method**: DM vs channel alerts
- **Command Permissions**: Who can use commands
- **Integration Scope**: Public vs private channels

#### Discord
- **Server Monitoring**: Select servers to monitor
- **Alert Permissions**: Who receives alerts
- **Command Restrictions**: Role-based command access
- **Channel Rules**: Per-channel analysis settings

## 📊 Analytics & Monitoring

### Usage Statistics
All integrations track:
- Total analyses performed
- Risk detection rates
- Average Guardian scores
- Response times
- Error rates

### Performance Metrics
Monitor integration performance:
- API response times
- Cache hit rates
- Memory usage
- Error frequencies
- Uptime statistics

### Export Capabilities
Export analytics data:
- CSV format for spreadsheet analysis
- JSON for custom processing
- PDF reports for management
- API access for real-time data

## 🛡️ Security Considerations

### API Security
- **Authentication**: Use secure API tokens
- **HTTPS**: Encrypt all API communications
- **Rate Limiting**: Prevent API abuse
- **Access Control**: Restrict who can use integrations

### Data Privacy
- **Local Processing**: All analysis happens on your server
- **No Data Collection**: Integrations don't store sensitive data
- **User Consent**: Be transparent about content analysis
- **Data Retention**: Configure how long to keep analysis results

### Compliance
- **GDPR**: Ensure compliance with data protection regulations
- **CCPA**: Follow California privacy laws
- **HIPAA**: Healthcare compliance for medical content
- **SOC2**: Security compliance for enterprise use

## 🔍 Troubleshooting

### Common Issues

**API Connection Failed**
1. Check if LRDEnE Guardian is running
2. Verify API endpoint URL
3. Test network connectivity
4. Check firewall settings

**Integration Not Responding**
1. Check bot/application status
2. Verify authentication tokens
3. Review error logs
4. Restart the integration

**False Positives**
1. Adjust risk thresholds
2. Configure content filters
3. Update analysis context
4. Train custom models

**Performance Issues**
1. Enable caching
2. Optimize API calls
3. Reduce analysis frequency
4. Scale infrastructure

### Debug Mode
Enable debug logging:
```bash
export LRDEN_GUARDIAN_DEBUG=true
```

Check logs for detailed error information and performance metrics.

## 🤝 Contributing

We welcome contributions for new integrations! Please:

1. **Fork the repository**
2. **Create integration branch**: `integrations/platform-name`
3. **Follow our patterns**: Use existing code structure
4. **Add documentation**: Include installation and usage guides
5. **Test thoroughly**: Verify with real content
6. **Submit pull request**: With detailed description

### Integration Guidelines
- **Error Handling**: Robust error management
- **Logging**: Comprehensive debug information
- **Configuration**: Flexible settings options
- **Security**: Follow security best practices
- **Performance**: Efficient API usage
- **Documentation**: Clear setup instructions

## 📄 License

Copyright (c) 2026 LRDEnE. All rights reserved.

## 🏢 About LRDEnE

LRDEnE is a leading provider of AI safety and content validation solutions. Our integration plugins extend Guardian's protection to the platforms where you work, communicate, and collaborate.

---

*🛡️ LRDEnE Guardian - Your AI Safety Partner*
