# 🛡️ LRDEnE Guardian Browser Extension

Real-time AI safety and hallucination detection while browsing the web.

## 🚀 Features

### Real-Time Protection
- **Live Content Analysis**: Automatically analyzes text as you browse
- **Smart Detection**: Identifies AI-generated content and potential risks
- **Visual Indicators**: Color-coded safety badges and warnings
- **Context-Aware**: Understands the context of different websites

### User-Friendly Interface
- **One-Click Analysis**: Right-click any text to analyze instantly
- **Floating Badge**: Real-time safety status indicator
- **Popup Interface**: Clean, modern popup for detailed analysis
- **Settings Panel**: Comprehensive configuration options

### Developer Features
- **API Integration**: Connects to LRDEnE Guardian API
- **Customizable**: Configure protected sites and analysis rules
- **Statistics**: Track usage and performance metrics
- **History**: View and manage analysis history

## 📦 Installation

### From Source
1. Clone the LRDEnE Guardian repository
2. Navigate to the `browser_extension` directory
3. Open Chrome and go to `chrome://extensions/`
4. Enable "Developer mode" (top right toggle)
5. Click "Load unpacked" and select the `browser_extension` directory
6. Ensure LRDEnE Guardian web dashboard is running on `http://localhost:5001`

### From Chrome Web Store
*(Coming soon)*

## 🔧 Configuration

### Basic Setup
1. Install the extension
2. Click the LRDEnE Guardian icon in your toolbar
3. Configure the API endpoint (default: `http://localhost:5001`)
4. Test the connection
5. Enable desired features

### Settings Options
- **API Endpoint**: URL of your LRDEnE Guardian server
- **Auto-Analyze**: Automatically analyze content on paste
- **Notifications**: Show warnings for risky content
- **Real-Time Protection**: Enable continuous monitoring
- **Protected Sites**: Sites where protection is always active

## 🌐 Usage

### Popup Analysis
1. Click the LRDEnE Guardian icon in your toolbar
2. Enter text or select text on the webpage
3. Click "Analyze Content" for instant results
4. View safety scores, risk levels, and recommendations

### Context Menu
1. Select any text on a webpage
2. Right-click and choose "Analyze with LRDEnE Guardian"
3. View detailed analysis results

### Real-Time Monitoring
1. Enable real-time protection in settings
2. Browse protected sites (Twitter, Facebook, Reddit, etc.)
3. See the floating badge showing safety status
4. Get automatic warnings for risky content

### Content Script Features
- **Text Input Monitoring**: Analyzes content as you type
- **AI Content Detection**: Identifies AI-generated text
- **Risk Highlighting**: Visual indicators for problematic content
- **Warning Overlays**: Full-page warnings for high-risk content

## 🛠️ Development

### File Structure
```
browser_extension/
├── manifest.json          # Extension configuration
├── popup/                 # Popup interface
│   ├── popup.html        # Popup HTML
│   └── popup.js          # Popup logic
├── background/           # Service worker
│   └── background.js     # Background script
├── content/              # Content scripts
│   ├── content.js        # Page analysis
│   └── content.css       # Page styles
├── options/              # Settings page
│   ├── options.html      # Settings HTML
│   └── options.js        # Settings logic
├── icons/                # Extension icons
└── README.md             # This file
```

### API Integration
The extension communicates with the LRDEnE Guardian API:

```javascript
// Analyze content
const response = await fetch(`${apiEndpoint}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        content: text,
        context: { source: 'browser_extension' }
    })
});
```

### Building Icons
Icons should be created in the following sizes:
- 16x16px - `icon16.png`
- 32x32px - `icon32.png`
- 48x48px - `icon48.png`
- 128x128px - `icon128.png`

Use the LRDEnE Guardian branding with shield icon and purple gradient.

## 🔒 Privacy & Security

### Data Handling
- **Local Processing**: All analysis happens on your local server
- **No Data Collection**: Extension doesn't collect personal data
- **Secure Communication**: HTTPS connections to API server
- **User Control**: You control what gets analyzed

### Permissions
- `activeTab`: Access current tab for analysis
- `storage`: Save settings and analysis history
- `scripting`: Inject content scripts for real-time analysis
- `contextMenus`: Add right-click menu options
- `notifications`: Show safety warnings

## 🐛 Troubleshooting

### Common Issues

**Extension not working**
1. Check if LRDEnE Guardian API is running on `http://localhost:5001`
2. Verify API endpoint in extension settings
3. Test connection in settings page
4. Check browser console for errors

**No analysis results**
1. Ensure API server is accessible
2. Check network connectivity
3. Verify API endpoint URL
4. Try refreshing the page

**Missing floating badge**
1. Enable real-time protection in settings
2. Check if current site is in protected sites list
3. Refresh the webpage
4. Check for script errors in console

**Context menu not working**
1. Select text first, then right-click
2. Check if extension has proper permissions
3. Restart browser if needed
4. Reinstall extension if problem persists

### Debug Mode
Enable debug mode by:
1. Go to `chrome://extensions/`
2. Find LRDEnE Guardian extension
3. Click "Inspect views: background page"
4. Check console for error messages

## 📈 Performance

### Optimization
- **Debounced Analysis**: Prevents excessive API calls
- **Caching**: Stores recent analysis results
- **Lazy Loading**: Loads features only when needed
- **Efficient Monitoring**: Smart content detection

### Resource Usage
- **Memory**: < 10MB typical usage
- **CPU**: Minimal impact on browsing performance
- **Network**: Only analyzes content when requested
- **Storage**: < 5MB for settings and history

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow Chrome extension best practices
- Ensure cross-browser compatibility
- Test with different content types
- Maintain performance standards
- Document new features

## 📄 License

Copyright (c) 2026 LRDEnE. All rights reserved.

## 🏢 About LRDEnE

LRDEnE is a leading provider of AI safety and content validation solutions. Our mission is to ensure the integrity and safety of AI-powered applications across industries.

---

*🛡️ LRDEnE Guardian - Your AI Safety Partner*
