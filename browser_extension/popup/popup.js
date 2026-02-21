// LRDEnE Guardian Extension Popup Script
class GuardianPopup {
    constructor() {
        this.apiEndpoint = 'http://localhost:5001';
        this.initializeElements();
        this.attachEventListeners();
        this.loadSettings();
        this.checkConnection();
    }
    
    initializeElements() {
        this.elements = {
            textInput: document.getElementById('textInput'),
            analyzeBtn: document.getElementById('analyzeBtn'),
            analyzeSelectionBtn: document.getElementById('analyzeSelectionBtn'),
            loadingDiv: document.getElementById('loadingDiv'),
            resultsDiv: document.getElementById('resultsDiv'),
            safetyStatus: document.getElementById('safetyStatus'),
            guardianScore: document.getElementById('guardianScore'),
            confidenceScore: document.getElementById('confidenceScore'),
            riskLevel: document.getElementById('riskLevel'),
            issuesSection: document.getElementById('issuesSection'),
            issuesList: document.getElementById('issuesList'),
            recommendationsSection: document.getElementById('recommendationsSection'),
            recommendationsList: document.getElementById('recommendationsList'),
            status: document.getElementById('status'),
            settingsBtn: document.getElementById('settingsBtn')
        };
    }
    
    attachEventListeners() {
        this.elements.analyzeBtn.addEventListener('click', () => this.analyzeText());
        this.elements.analyzeSelectionBtn.addEventListener('click', () => this.analyzeSelection());
        this.elements.settingsBtn.addEventListener('click', () => this.openSettings());
        
        // Auto-analyze on paste
        this.elements.textInput.addEventListener('paste', () => {
            setTimeout(() => this.analyzeText(), 100);
        });
        
        // Get selected text on popup open
        this.getSelectedText();
    }
    
    async loadSettings() {
        try {
            const settings = await chrome.storage.sync.get({
                apiEndpoint: this.apiEndpoint,
                autoAnalyze: true,
                showNotifications: true
            });
            
            this.apiEndpoint = settings.apiEndpoint;
            this.autoAnalyze = settings.autoAnalyze;
            this.showNotifications = settings.showNotifications;
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }
    
    async checkConnection() {
        try {
            const response = await fetch(`${this.apiEndpoint}/api-info`);
            if (response.ok) {
                this.updateStatus('Connected to LRDEnE Guardian', 'safe');
            } else {
                this.updateStatus('Guardian API unavailable', 'warning');
            }
        } catch (error) {
            this.updateStatus('Connection failed', 'danger');
            this.elements.analyzeBtn.disabled = true;
            this.elements.analyzeSelectionBtn.disabled = true;
        }
    }
    
    updateStatus(message, type = 'safe') {
        const statusDiv = this.elements.status;
        statusDiv.className = `status ${type}`;
        
        const icons = {
            safe: 'fas fa-check-circle',
            warning: 'fas fa-exclamation-triangle',
            danger: 'fas fa-times-circle'
        };
        
        statusDiv.innerHTML = `<i class="${icons[type]}"></i><span>${message}</span>`;
    }
    
    async getSelectedText() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            const results = await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: () => window.getSelection().toString().trim()
            });
            
            if (results && results[0] && results[0].result) {
                this.elements.textInput.value = results[0].result;
                if (this.autoAnalyze) {
                    setTimeout(() => this.analyzeText(), 500);
                }
            }
        } catch (error) {
            console.error('Error getting selected text:', error);
        }
    }
    
    async analyzeText() {
        const content = this.elements.textInput.value.trim();
        
        if (!content) {
            this.showNotification('Please enter text to analyze', 'warning');
            return;
        }
        
        this.showLoading(true);
        this.hideResults();
        
        try {
            const response = await fetch(`${this.apiEndpoint}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    context: {
                        source: 'browser_extension',
                        url: await this.getCurrentUrl()
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            this.displayResults(result);
            
            if (this.showNotifications) {
                this.showNotification('Analysis completed!', 'success');
            }
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Analysis failed. Please check your connection.', 'error');
            this.updateStatus('Analysis failed', 'danger');
        } finally {
            this.showLoading(false);
        }
    }
    
    async analyzeSelection() {
        await this.getSelectedText();
        if (this.elements.textInput.value.trim()) {
            await this.analyzeText();
        } else {
            this.showNotification('No text selected on the page', 'warning');
        }
    }
    
    async getCurrentUrl() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            return tab.url;
        } catch (error) {
            return 'unknown';
        }
    }
    
    showLoading(show) {
        this.elements.loadingDiv.style.display = show ? 'block' : 'none';
        this.elements.analyzeBtn.disabled = show;
        this.elements.analyzeSelectionBtn.disabled = show;
        
        if (show) {
            this.elements.analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        } else {
            this.elements.analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Content';
        }
    }
    
    hideResults() {
        this.elements.resultsDiv.classList.remove('show');
    }
    
    displayResults(result) {
        this.elements.resultsDiv.classList.add('show');
        
        // Safety Status
        const safetyStatus = result.is_safe ? '✅ SAFE' : '⚠️ REQUIRES REVIEW';
        this.elements.safetyStatus.textContent = safetyStatus;
        this.elements.safetyStatus.style.color = result.is_safe ? '#4ecdc4' : '#ff6b6b';
        
        // Metrics
        this.elements.guardianScore.textContent = result.guardian_score.toFixed(3);
        this.elements.confidenceScore.textContent = `${(result.confidence_score * 100).toFixed(1)}%`;
        this.elements.riskLevel.textContent = result.risk_level.toUpperCase();
        this.elements.riskLevel.style.color = this.getRiskColor(result.risk_level);
        
        // Issues
        if (result.detected_issues && result.detected_issues.length > 0) {
            this.elements.issuesSection.style.display = 'block';
            this.elements.issuesList.innerHTML = result.detected_issues
                .map(issue => `<li>${issue}</li>`)
                .join('');
        } else {
            this.elements.issuesSection.style.display = 'none';
        }
        
        // Recommendations
        if (result.recommendations && result.recommendations.length > 0) {
            this.elements.recommendationsSection.style.display = 'block';
            this.elements.recommendationsList.innerHTML = result.recommendations
                .map(rec => `<li>${rec}</li>`)
                .join('');
        } else {
            this.elements.recommendationsSection.style.display = 'none';
        }
        
        // Update status
        this.updateStatus('Analysis complete', result.is_safe ? 'safe' : 'warning');
    }
    
    getRiskColor(riskLevel) {
        const colors = {
            low: '#4ecdc4',
            medium: '#f7b733',
            high: '#fc4a1a',
            critical: '#eb3349'
        };
        return colors[riskLevel] || '#666';
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 10px 15px;
            border-radius: 8px;
            color: white;
            font-size: 14px;
            z-index: 10000;
            max-width: 300px;
            word-wrap: break-word;
        `;
        
        const colors = {
            success: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
            warning: 'linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%)',
            error: 'linear-gradient(135deg, #eb3349 0%, #f45c43 100%)',
            info: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        };
        
        notification.style.background = colors[type] || colors.info;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    openSettings() {
        chrome.runtime.openOptionsPage();
    }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GuardianPopup();
});
