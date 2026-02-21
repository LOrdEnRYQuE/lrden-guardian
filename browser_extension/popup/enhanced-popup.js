// LRDEnE Guardian Enhanced Browser Extension Popup
// Enhanced UI/UX with modern interactions and animations

class EnhancedPopup {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.loadingStates = {
            analyzing: false,
            demo: false
        };
        this.cache = new Map();
    }

    initializeElements() {
        this.contentInput = document.getElementById('contentInput');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.demoBtn = document.getElementById('demoBtn');
        this.settingsBtn = document.getElementById('settingsBtn');
        this.deepAnalysis = document.getElementById('deepAnalysis');
        this.checkSources = document.getElementById('checkSources');
        this.resultsContainer = document.getElementById('resultsContainer');
    }

    attachEventListeners() {
        // Content input events
        if (this.contentInput) {
            this.contentInput.addEventListener('input', () => this.updateCharCount());
            this.contentInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                    e.preventDefault();
                    this.analyzeContent();
                }
            });
        }
        
        // Button events
        if (this.analyzeBtn) {
            this.analyzeBtn.addEventListener('click', () => this.analyzeContent());
        }
        
        if (this.clearBtn) {
            this.clearBtn.addEventListener('click', () => this.clearContent());
        }
        
        if (this.demoBtn) {
            this.demoBtn.addEventListener('click', () => this.loadDemoContent());
        }
        
        if (this.settingsBtn) {
            this.settingsBtn.addEventListener('click', () => this.openSettings());
        }
        
        // Auto-save content
        if (this.contentInput) {
            let saveTimeout;
            this.contentInput.addEventListener('input', () => {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    this.saveDraft();
                }, 1000);
            });
        }
        
        // Load draft on load
        this.loadDraft();
    }

    updateCharCount() {
        const count = this.contentInput.value.length;
        const maxLength = this.contentInput.maxLength;
        
        // Update character count display
        const charCount = document.querySelector('.char-count');
        if (charCount) {
            charCount.textContent = `${count}/${maxLength}`;
            
            // Update color based on length
            if (count > maxLength * 0.9) {
                charCount.classList.add('text-red-500');
                charCount.classList.remove('text-gray-500');
            } else {
                charCount.classList.remove('text-red-500');
                charCount.classList.add('text-gray-500');
            }
        }
        
        // Enable/disable analyze button
        this.analyzeBtn.disabled = count < 10;
    }

    clearContent() {
        this.contentInput.value = '';
        this.updateCharCount();
        this.contentInput.focus();
        
        // Add clear animation
        this.contentInput.classList.add('fade-in');
        setTimeout(() => {
            this.contentInput.classList.remove('fade-in');
        }, 300);
        
        this.resultsContainer.classList.add('hidden');
    }

    async analyzeContent() {
        const content = this.contentInput.value.trim();
        
        if (!content) {
            this.showNotification('Please enter some content to analyze', 'warning');
            return;
        }
        
        if (content.length < 10) {
            this.showNotification('Content is too short for meaningful analysis', 'warning');
            return;
        }
        
        this.setLoadingState('analyzing', true);
        
        try {
            const result = await this.callGuardianAPI(content);
            this.displayResults(result);
            this.saveToHistory(result);
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            this.setLoadingState('analyzing', false);
        }
    }

    async callGuardianAPI(content) {
        const cacheKey = this.generateCacheKey(content);
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }
        
        // Call the API
        const response = await fetch('http://localhost:5001/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: content,
                context: {
                    source: 'browser_extension',
                    timestamp: new Date().toISOString(),
                    deep_analysis: this.deepAnalysis?.checked,
                    check_sources: this.checkSources?.checked
                }
            })
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        const result = await response.json();
        
        // Cache the result
        this.cache.set(cacheKey, result);
        
        // Limit cache size
        if (this.cache.size > 100) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        
        return result;
    }

    displayResults(result) {
        this.resultsContainer.classList.remove('hidden');
        
        const riskClass = result.is_safe ? 'safe' : result.risk_level === 'high' ? 'danger' : 'warning';
        const statusIcon = result.is_safe ? '✅' : '⚠️';
        const statusText = result.is_safe ? 'Safe Content' : 'Requires Review';
        
        const resultsHtml = `
            <div class="result-card ${riskClass}">
                <div class="result-header">
                    <div class="result-status">
                        <div class="status-icon ${riskClass}">
                            ${statusIcon}
                        </div>
                        <div>
                            <div class="result-title">${statusText}</div>
                            <div class="result-score">Score: ${result.guardian_score?.toFixed(3) || '0.000'}</div>
                        </div>
                    </div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value">${(100 * (result.confidence_score || 0)).toFixed(1)}%</div>
                        <div class="stat-label">Confidence</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.guardian_score?.toFixed(3) || '0.000'}</div>
                        <div class="stat-label">Guardian Score</div>
                    </div>
                    <div class="stat-item">
                        <div class="status-icon ${riskClass}">
                            ${statusIcon}
                        </div>
                        <div class="stat-label">Status</div>
                    </div>
                </div>
                
                ${result.analysis_summary ? `
                <div class="result-summary">
                    ${result.analysis_summary}
                </div>
                ` : ''}
                
                ${result.detected_issues && result.detected_issues.length > 0 ? `
                <div class="result-issues">
                    <h6>Issues Detected</h6>
                    ${result.detected_issues.slice(0, 3).map(issue => `
                        <div class="issue-item">
                            <i class="ri-error-warning-line"></i>
                            ${issue}
                        </div>
                    `).join('')}
                </div>
                ` : ''}
                
                ${result.recommendations && result.recommendations.length > 0 ? `
                <div class="result-recommendations">
                    <h6>Recommendations</h6>
                    ${result.recommendations.slice(0, 3).map(rec => `
                        <div class="recommendation-item">
                            <i class="ri-arrow-right-line"></i>
                            ${rec}
                        </div>
                    `).join('')}
                </div>
                ` : ''}
                
                <div class="result-actions">
                    <button class="btn btn-secondary btn-small" onclick="enhancedPopup.shareResults()">
                        <i class="ri-share-line"></i>Share
                    </button>
                    <button class="btn btn-secondary btn-small" onclick="enhancedPopup.exportResults()">
                        <i class="ri-download-line"></i>Export
                    </button>
                </div>
            </div>
        `;
        
        this.resultsContainer.innerHTML = resultsHtml;
        
        // Scroll to results
        this.resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Add entrance animation
        setTimeout(() => {
            const resultCard = this.resultsContainer.querySelector('.result-card');
            if (resultCard) {
                resultCard.classList.add('slide-in');
            }
        }, 100);
    }

    loadDemoContent() {
        const demoContent = `As an AI language model, I can provide you with comprehensive information about various topics. However, I must clarify that while I strive to be accurate, I may occasionally generate responses that contain inaccuracies or "hallucinations" - statements that appear factual but are not actually correct.

I have access to a vast amount of training data, but my knowledge has a cutoff date, so I may not have information about very recent events. Additionally, I cannot browse the internet in real-time or access proprietary databases.

For the most accurate and up-to-date information, I recommend verifying critical information through primary sources, academic journals, or official documentation. This is especially important for medical, legal, financial, or safety-critical information.`;
        
        this.contentInput.value = demoContent;
        this.updateCharCount();
        
        // Add typing animation
        this.contentInput.classList.add('fade-in');
        setTimeout(() => {
            this.contentInput.classList.remove('fade-in');
        }, 100);
        
        this.showNotification('Demo content loaded. This contains AI indicators for testing.', 'info');
    }

    saveDraft() {
        const content = this.contentInput.value;
        if (content) {
            localStorage.setItem('lrden_draft_content', content);
        }
    }

    loadDraft() {
        const draft = localStorage.getItem('lrden_draft_content');
        if (draft && !this.contentInput.value) {
            this.contentInput.value = draft;
            this.updateCharCount();
        }
    }

    saveToHistory(result) {
        const history = JSON.parse(localStorage.getItem('lrden_history') || '[]');
        
        const historyItem = {
            id: Date.now(),
            content: this.contentInput.value.substring(0, 100),
            result: result,
            timestamp: new Date().toISOString()
        };
        
        history.unshift(historyItem);
        
        // Keep only last 50 items
        if (history.length > 50) {
            history.splice(50);
        }
        
        localStorage.setItem('lrden_history', JSON.stringify(history));
    }

    setLoadingState(type, loading) {
        this.loadingStates[type] = loading;
        
        // Update button states
        if (type === 'analyzing') {
            this.analyzeBtn.disabled = loading;
            if (loading) {
                this.analyzeBtn.innerHTML = '<i class="ri-loader-4-line loading-spinner"></i>Analyzing...';
            } else {
                this.analyzeBtn.innerHTML = '<i class="ri-search-line btn-icon"></i>Analyze';
            }
        }
        
        if (type === 'demo') {
            this.demoBtn.disabled = loading;
            if (loading) {
                this.demoBtn.innerHTML = '<i class="ri-loader-4-line loading-spinner"></i>Loading...';
            } else {
                this.demoBtn.innerHTML = '<i class="ri-magic-line"></i>Demo';
            }
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 fade-in max-w-sm`;
        
        // Style based on type
        const colors = {
            info: 'bg-blue-500 text-white',
            success: 'bg-green-500 text-white',
            warning: 'bg-yellow-500 text-white',
            error: 'bg-red-500 text-white'
        };
        
        notification.className += ` ${colors[type]}`;
        
        // Add content
        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                <i class="ri-${type === 'info' ? 'information' : type === 'success' ? 'checkbox-circle' : type === 'warning' ? 'alert' : 'error'}"></i>
                <div>
                    <div class="font-semibold">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
                    <div class="text-sm opacity-90">${message}</div>
                </div>
                <button onclick="this.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                    <i class="ri-close-line"></i>
                </button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }

    shareResults() {
        // Implement share functionality
        if (navigator.share) {
            navigator.share({
                title: 'LRDEnE Guardian Analysis Results',
                text: 'Check out my AI safety analysis results',
                url: 'https://github.com/LOrdEnRYQuE/lrden-guardian'
            });
        } else {
            this.copyToClipboard(window.location.href);
            this.showNotification('Link copied to clipboard', 'success');
        }
    }

    exportResults() {
        const results = this.resultsContainer.innerHTML;
        const blob = new Blob([results], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `lrden-guardian-analysis-${Date.now()}.txt`;
        a.click();
        
        URL.revokeObjectURL(url);
        this.showNotification('Results exported successfully', 'success');
    }

    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showNotification('Copied to clipboard', 'success');
        }).catch(err => {
            console.error('Failed to copy text:', err);
        });
    }

    openSettings() {
        // Open settings page
        chrome.runtime.openOptionsPage();
    }

    // Initialize the enhanced popup
    static init() {
        window.enhancedPopup = new EnhancedPopup();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    EnhancedPopup.init();
});
