// LRDEnE Guardian Content Script
class GuardianContent {
    constructor() {
        this.apiEndpoint = 'http://localhost:5001';
        this.isAnalyzing = false;
        this.badge = null;
        this.initializeElements();
        this.attachEventListeners();
        this.loadSettings();
        this.initializeRealTimeProtection();
    }
    
    initializeElements() {
        // Create floating badge for real-time feedback
        this.createFloatingBadge();
    }
    
    createFloatingBadge() {
        this.badge = document.createElement('div');
        this.badge.id = 'lrden-guardian-badge';
        this.badge.innerHTML = `
            <div class="guardian-badge-content">
                <i class="fas fa-shield-alt"></i>
                <span class="guardian-text">LRDEnE Guardian</span>
                <div class="guardian-status"></div>
            </div>
        `;
        
        this.badge.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 15px;
            border-radius: 25px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 12px;
            z-index: 10000;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            max-width: 200px;
            opacity: 0.9;
        `;
        
        this.badge.addEventListener('mouseenter', () => {
            this.badge.style.opacity = '1';
            this.badge.style.transform = 'scale(1.05)';
        });
        
        this.badge.addEventListener('mouseleave', () => {
            this.badge.style.opacity = '0.9';
            this.badge.style.transform = 'scale(1)';
        });
        
        this.badge.addEventListener('click', () => {
            this.openExtensionPopup();
        });
        
        document.body.appendChild(this.badge);
    }
    
    attachEventListeners() {
        // Monitor text inputs and textareas for real-time analysis
        document.addEventListener('input', (event) => {
            if (this.settings.realTimeProtection) {
                this.handleTextInput(event);
            }
        });
        
        // Monitor paste events
        document.addEventListener('paste', (event) => {
            if (this.settings.realTimeProtection) {
                setTimeout(() => this.handleTextInput(event), 100);
            }
        });
        
        // Monitor AI-generated content indicators
        this.monitorAIContent();
    }
    
    async loadSettings() {
        try {
            const response = await chrome.runtime.sendMessage({ action: 'getSettings' });
            if (response.success) {
                this.settings = response.settings;
                this.apiEndpoint = this.settings.apiEndpoint;
            }
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }
    
    initializeRealTimeProtection() {
        // Check if current site should be protected
        if (this.shouldProtectSite()) {
            this.startRealTimeMonitoring();
        }
    }
    
    shouldProtectSite() {
        const hostname = window.location.hostname;
        return this.settings.protectedSites.some(site => 
            hostname.includes(site) || site.includes(hostname)
        );
    }
    
    startRealTimeMonitoring() {
        // Monitor for new content being added to the page
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        this.checkNewContent(node);
                    }
                });
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    checkNewContent(node) {
        // Check if new node contains significant text content
        const textContent = node.textContent || '';
        if (textContent.length > 100 && !this.isAnalyzing) {
            this.analyzeContent(textContent, 'auto_monitor');
        }
    }
    
    handleTextInput(event) {
        const target = event.target;
        
        // Only analyze text inputs and textareas with significant content
        if ((target.tagName === 'INPUT' && target.type === 'text') || 
            target.tagName === 'TEXTAREA') {
            
            const content = target.value.trim();
            if (content.length > 50 && !this.isAnalyzing) {
                this.analyzeContent(content, 'real_time_input');
            }
        }
    }
    
    monitorAIContent() {
        // Look for AI-generated content indicators
        const aiIndicators = [
            'As an AI language model',
            'I cannot provide',
            'I don\'t have access',
            'As an AI assistant',
            'I\'m an AI',
            'I am an AI'
        ];
        
        const pageText = document.body.textContent || '';
        const hasAIIndicator = aiIndicators.some(indicator => 
            pageText.toLowerCase().includes(indicator.toLowerCase())
        );
        
        if (hasAIIndicator) {
            this.updateBadgeStatus('AI Content Detected', 'warning');
        }
    }
    
    async analyzeContent(content, source = 'manual') {
        if (this.isAnalyzing || content.length < 10) return;
        
        this.isAnalyzing = true;
        this.updateBadgeStatus('Analyzing...', 'analyzing');
        
        try {
            const response = await chrome.runtime.sendMessage({
                action: 'analyze',
                content: content,
                context: {
                    source: source,
                    url: window.location.href,
                    title: document.title,
                    timestamp: new Date().toISOString()
                }
            });
            
            if (response.success) {
                this.handleAnalysisResult(response.result);
            } else {
                this.updateBadgeStatus('Analysis Failed', 'error');
            }
            
        } catch (error) {
            console.error('Content analysis error:', error);
            this.updateBadgeStatus('Connection Error', 'error');
        } finally {
            this.isAnalyzing = false;
        }
    }
    
    handleAnalysisResult(result) {
        const status = result.is_safe ? 'Safe' : 'Risk Detected';
        const type = result.is_safe ? 'safe' : 'warning';
        
        this.updateBadgeStatus(status, type);
        
        // Show detailed tooltip on hover
        this.badge.title = `
Guardian Score: ${result.guardian_score.toFixed(3)}
Confidence: ${(result.confidence_score * 100).toFixed(1)}%
Risk Level: ${result.risk_level.toUpperCase()}
${result.detected_issues.length > 0 ? '\nIssues: ' + result.detected_issues.slice(0, 2).join(', ') : ''}
        `.trim();
        
        // Save to history
        chrome.runtime.sendMessage({
            action: 'saveToHistory',
            analysis: {
                ...result,
                url: window.location.href,
                title: document.title
            }
        });
        
        // Show warning for risky content
        if (!result.is_safe && this.settings.showNotifications) {
            this.showPageWarning(result);
        }
    }
    
    updateBadgeStatus(text, type) {
        const statusElement = this.badge.querySelector('.guardian-status');
        statusElement.textContent = text;
        
        // Update badge color based on type
        const colors = {
            safe: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
            warning: 'linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%)',
            error: 'linear-gradient(135deg, #eb3349 0%, #f45c43 100%)',
            analyzing: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        };
        
        this.badge.style.background = colors[type] || colors.analyzing;
    }
    
    showPageWarning(result) {
        // Create warning overlay
        const warning = document.createElement('div');
        warning.innerHTML = `
            <div class="guardian-warning-overlay">
                <div class="guardian-warning-content">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>⚠️ Content Warning</h3>
                    <p>LRDEnE Guardian detected potential issues with this content:</p>
                    <ul>
                        ${result.detected_issues.slice(0, 3).map(issue => `<li>${issue}</li>`).join('')}
                    </ul>
                    <button onclick="this.parentElement.parentElement.remove()">Dismiss</button>
                </div>
            </div>
        `;
        
        warning.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        const content = warning.querySelector('.guardian-warning-content');
        content.style.cssText = `
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 500px;
            text-align: center;
            color: #333;
        `;
        
        document.body.appendChild(warning);
        
        // Auto-dismiss after 10 seconds
        setTimeout(() => {
            if (warning.parentElement) {
                warning.remove();
            }
        }, 10000);
    }
    
    openExtensionPopup() {
        // Send message to background to open popup
        chrome.runtime.sendMessage({ action: 'openPopup' });
    }
}

// Initialize content script
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new GuardianContent());
} else {
    new GuardianContent();
}
