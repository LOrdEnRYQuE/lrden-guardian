# 🔌 LRDEnE Guardian IDE Integrations

**AI Safety and Hallucination Detection for Your Development Environment**

LRDEnE Guardian provides comprehensive IDE integrations to protect developers from AI-generated code issues, hallucinations, and security vulnerabilities right where they work.

---

## 🚀 **Available IDE Integrations**

### 🎯 **VS Code Extension**
**File**: `vscode/lrden-guardian-vscode/`

**Features:**
- **Real-time Analysis**: Automatic code analysis as you type
- **Visual Indicators**: Color-coded safety decorations in the editor
- **Context Menu**: Right-click analysis for any selection
- **Command Palette**: Quick access to all features
- **Activity Bar**: Dedicated Guardian panel with results
- **Status Bar**: Real-time connection status
- **Project Analysis**: Bulk analysis of entire projects
- **Configuration**: Flexible settings and preferences

**Installation:**
```bash
# Install from VS Code Marketplace
code --install-extension lrden-guardian-vscode

# Or install from source
cd ide_integrations/vscode/lrden-guardian-vscode
npm install
npm run compile
code --install-extension .
```

**Usage:**
- Automatic analysis of AI-generated code
- Manual analysis via context menu
- Project-wide safety reports
- Real-time risk indicators

---

### 🎯 **Cursor Integration**
**File**: `cursor/lrden-guardian-cursor.py`

**Features:**
- **Workspace Monitoring**: Real-time file change detection
- **AI Content Detection**: Identifies AI-generated code patterns
- **Hallucination Checking**: Flags overconfident statements
- **Auto-Analysis**: Configurable automatic analysis
- **Integration Scripts**: Custom Cursor rules and automation
- **Configuration Management**: Persistent settings

**Installation:**
```bash
# Setup integration
python ide_integrations/cursor/lrden-guardian-cursor.py setup

# Monitor workspace
python ide_integrations/cursor/lrden-guardian-cursor.py monitor

# Analyze specific file
python ide_integrations/cursor/lrden-guardian-cursor.py analyze <file>
```

**Usage:**
- Monitor entire Cursor workspace
- Automatic analysis of new/modified files
- AI content pattern detection
- Custom analysis rules

---

### 🎯 **Universal Integration**
**File**: `general/lrden-guardian-universal.py`

**Features:**
- **Multi-IDE Support**: Works with any IDE supporting external tools
- **CLI Interface**: Command-line analysis for any file
- **Auto-Detection**: Automatically detects running IDE
- **Flexible Configuration**: Customizable settings
- **Cache Management**: Performance optimization
- **Batch Processing**: Analyze multiple files

**Supported IDEs:**
- Cursor
- Windsurf
- Antigravity
- Bolt
- Lovable
- And any IDE with external tool support

**Installation:**
```bash
# Make script executable
chmod +x ide_integrations/general/lrden-guardian-universal.py

# Analyze file
python ide_integrations/general/lrden-guardian-universal.py analyze <file>

# Check status
python ide_integrations/general/lrden-guardian-universal.py status

# Monitor workspace
python ide_integrations/general/lrden-guardian-universal.py monitor
```

---

## 🔧 **Common Features Across All Integrations**

### 🛡️ **Core Capabilities**
- **Real-time Analysis**: Sub-10ms processing speed
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, PHP, Ruby, Markdown
- **Risk Assessment**: 4-level risk classification
- **Guardian Score**: Proprietary 0.0-1.0 safety rating
- **Confidence Metrics**: Analysis certainty assessment
- **Issue Detection**: Specific problem identification
- **Recommendations**: Context-aware improvement suggestions

### 🎯 **AI Content Detection**
- **AI Indicators**: Identifies AI-generated code patterns
- **Hallucination Patterns**: Flags overconfident statements
- **Uncertainty Areas**: Highlights ambiguous content
- **Source Attribution**: Tracks content origins

### 📊 **Analytics & Monitoring**
- **Usage Statistics**: Track analysis frequency and results
- **Performance Metrics**: Monitor API response times
- **Risk Trends**: Identify patterns in risky content
- **Cache Management**: Optimize for performance

### 🔒 **Security & Privacy**
- **Local Processing**: All analysis happens on your machine
- **No Data Collection**: We don't store or analyze your code
- **Encrypted Communication**: HTTPS/TLS for API calls
- **Access Control**: Role-based permissions and authentication

---

## 🚀 **Quick Start Guide**

### 1. **Start LRDEnE Guardian API**
```bash
cd web_dashboard
python app.py
```

### 2. **Choose Your IDE Integration**

#### **VS Code (Recommended)**
```bash
# Install from marketplace
code --install-extension lrden-guardian-vscode
```

#### **Cursor**
```bash
python ide_integrations/cursor/lrden-guardian-cursor.py setup
```

#### **Other IDEs**
```bash
python ide_integrations/general/lrden-guardian-universal.py
```

### 3. **Configure Settings**
- Set API endpoint: `http://localhost:5001`
- Choose analysis frequency
- Configure risk thresholds
- Enable notifications

### 4. **Start Using**
- Write code normally
- Get real-time safety feedback
- Review analysis results
- Fix identified issues

---

## 📋 **Configuration Options**

### **Common Settings**
```json
{
  "api_endpoint": "http://localhost:5001",
  "auto_analysis": true,
  "analysis_delay": 1000,
  "show_decorations": true,
  "show_notifications": true,
  "risk_threshold": "medium",
  "supported_languages": ["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust", "php", "ruby", "markdown"]
}
```

### **IDE-Specific Settings**

#### **VS Code**
```json
{
  "lrdenGuardian.apiEndpoint": "http://localhost:5001",
  "lrdenGuardian.autoAnalysis": true,
  "lrdenGuardian.showDecorations": true,
  "lrdenGuardian.riskThreshold": "medium"
}
```

#### **Cursor**
```json
{
  "api_endpoint": "http://localhost:5001",
  "auto_analyze": true,
  "analysis_delay": 1.0,
  "risk_threshold": "medium"
}
```

---

## 🔍 **Detection Capabilities**

### 🤖 **AI Hallucination Patterns**
- **Overconfident Statements**: "definitely", "absolutely", "guaranteed"
- **Impossible Claims**: "never fails", "always succeeds", "perfectly accurate"
- **Vague Assertions**: Uncertain or ambiguous statements
- **False Authority Claims**: Claims of knowledge without sources

### 🛡️ **Security Vulnerabilities**
- **Hardcoded Secrets**: API keys, passwords, tokens
- **Insecure Functions**: eval(), exec(), shell commands
- **SQL Injection Risks**: Unsafe database queries
- **Path Traversal**: File system access vulnerabilities
- **XSS Vectors**: Cross-site scripting risks

### 📝 **Code Quality Issues**
- **Error Handling**: Missing or inadequate error handling
- **Input Validation**: Lack of input sanitization
- **Resource Management**: Memory leaks, unclosed files
- **Performance Issues**: Inefficient algorithms, bottlenecks

---

## 📈 **Performance & Optimization**

### ⚡ **Speed**
- **Analysis Time**: < 10ms average
- **Cache Hit Rate**: 90%+ for repeated content
- **Memory Usage**: < 50MB typical
- **CPU Impact**: Minimal on IDE performance

### 🗄️ **Caching Strategy**
- **Content Hashing**: SHA-256 based content identification
- **Time-Based Expiration**: 24-hour cache lifetime
- **Size Limiting**: 1000 items maximum
- **LRU Eviction**: Least recently used removal

### 🔄 **Background Processing**
- **Async Analysis**: Non-blocking content analysis
- **Queue Management**: Prevents API overload
- **Retry Logic**: Automatic retry on failures
- **Error Handling**: Graceful degradation

---

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **API Connection Failed**
1. Check if LRDEnE Guardian is running: `python web_dashboard/app.py`
2. Verify API endpoint: `http://localhost:5001/api-info`
3. Check network connectivity and firewall settings

#### **Extension Not Working**
1. Restart your IDE
2. Check extension logs for errors
3. Verify API endpoint configuration
4. Update to latest version

#### **Performance Issues**
1. Increase analysis delay in settings
2. Clear cache to free memory
3. Check system resources
4. Reduce concurrent analyses

#### **False Positives**
1. Adjust risk threshold settings
2. Add custom patterns to ignore list
3. Update AI indicator patterns
4. Provide feedback for improvement

### **Debug Mode**
Enable detailed logging:
```bash
export LRDEN_GUARDIAN_DEBUG=true
```

Check logs:
- VS Code: `Help > Toggle Developer Tools`
- Cursor: Check integration script output
- Universal: Check console output

---

## 🤝 **Contributing**

### **Adding New IDE Support**
1. Create new integration directory: `ide_integrations/<ide-name>/`
2. Follow existing patterns and structure
3. Implement IDE-specific features
4. Add comprehensive documentation
5. Submit pull request

### **Development Guidelines**
- Follow existing code style and patterns
- Include comprehensive error handling
- Add proper logging and debugging
- Write clear documentation
- Test with real AI-generated content

### **Testing**
- Test with various AI-generated code samples
- Verify performance with large files
- Test edge cases and error conditions
- Validate configuration options

---

## 📄 **License**

Copyright (c) 2026 LRDEnE. All rights reserved.

## 🏢 **About LRDEnE**

LRDEnE is a leading provider of AI safety and content validation solutions. Our IDE integrations extend Guardian's protection to the development environment where AI-generated code is most prevalent.

---

*🛡️ LRDEnE Guardian - Your AI Safety Partner in Development*
