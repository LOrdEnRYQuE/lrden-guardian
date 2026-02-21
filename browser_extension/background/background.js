// LRDEnE Guardian Background Service Worker
class GuardianBackground {
    constructor() {
        this.initializeEventListeners();
        this.initializeContextMenu();
        this.loadSettings();
    }
    
    initializeEventListeners() {
        // Extension installation
        chrome.runtime.onInstalled.addListener((details) => {
            if (details.reason === 'install') {
                this.handleInstall();
            } else if (details.reason === 'update') {
                this.handleUpdate(details.previousVersion);
            }
        });
        
        // Context menu clicks
        chrome.contextMenus.onClicked.addListener((info, tab) => {
            if (info.menuItemId === 'analyze-selection') {
                this.handleContextMenuAnalysis(info, tab);
            }
        });
        
        // Action button click (fallback for older Chrome versions)
        chrome.action.onClicked.addListener((tab) => {
            this.openPopup(tab);
        });
        
        // Message handling
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
            return true; // Keep message channel open for async response
        });
    }
    
    async initializeContextMenu() {
        try {
            await chrome.contextMenus.removeAll();
            
            chrome.contextMenus.create({
                id: 'analyze-selection',
                title: 'Analyze with LRDEnE Guardian',
                contexts: ['selection'],
                documentUrlPatterns: ['http://*/*', 'https://*/*']
            });
            
            chrome.contextMenus.create({
                id: 'analyze-page',
                title: 'Analyze Page Content',
                contexts: ['page'],
                documentUrlPatterns: ['http://*/*', 'https://*/*']
            });
            
        } catch (error) {
            console.error('Error creating context menus:', error);
        }
    }
    
    async loadSettings() {
        try {
            const settings = await chrome.storage.sync.get({
                apiEndpoint: 'http://localhost:5001',
                autoAnalyze: true,
                showNotifications: true,
                realTimeProtection: false,
                protectedSites: ['twitter.com', 'facebook.com', 'reddit.com']
            });
            
            this.settings = settings;
        } catch (error) {
            console.error('Error loading settings:', error);
            this.settings = {
                apiEndpoint: 'http://localhost:5001',
                autoAnalyze: true,
                showNotifications: true,
                realTimeProtection: false,
                protectedSites: ['twitter.com', 'facebook.com', 'reddit.com']
            };
        }
    }
    
    async handleInstall() {
        // Set default settings
        await chrome.storage.sync.set({
            apiEndpoint: 'http://localhost:5001',
            autoAnalyze: true,
            showNotifications: true,
            realTimeProtection: false,
            protectedSites: ['twitter.com', 'facebook.com', 'reddit.com'],
            analysisHistory: []
        });
        
        // Open welcome page
        chrome.tabs.create({
            url: chrome.runtime.getURL('options/welcome.html')
        });
        
        // Show notification
        this.showNotification('LRDEnE Guardian installed successfully!', 'success');
    }
    
    handleUpdate(previousVersion) {
        console.log(`Updated from version ${previousVersion}`);
        this.showNotification('LRDEnE Guardian updated!', 'info');
    }
    
    async handleContextMenuAnalysis(info, tab) {
        if (info.selectionText) {
            // Store selected text for popup
            await chrome.storage.local.set({
                selectedText: info.selectionText,
                sourceUrl: info.pageUrl
            });
            
            // Open popup
            chrome.action.openPopup();
        }
    }
    
    async openPopup(tab) {
        chrome.action.openPopup();
    }
    
    async handleMessage(message, sender, sendResponse) {
        try {
            switch (message.action) {
                case 'analyze':
                    const result = await this.analyzeContent(message.content, message.context);
                    sendResponse({ success: true, result });
                    break;
                    
                case 'checkConnection':
                    const connected = await this.checkApiConnection();
                    sendResponse({ success: true, connected });
                    break;
                    
                case 'getSettings':
                    await this.loadSettings();
                    sendResponse({ success: true, settings: this.settings });
                    break;
                    
                case 'updateSettings':
                    await chrome.storage.sync.set(message.settings);
                    await this.loadSettings();
                    sendResponse({ success: true });
                    break;
                    
                case 'getAnalysisHistory':
                    const history = await this.getAnalysisHistory();
                    sendResponse({ success: true, history });
                    break;
                    
                case 'saveToHistory':
                    await this.saveToHistory(message.analysis);
                    sendResponse({ success: true });
                    break;
                    
                default:
                    sendResponse({ success: false, error: 'Unknown action' });
            }
        } catch (error) {
            console.error('Background script error:', error);
            sendResponse({ success: false, error: error.message });
        }
    }
    
    async analyzeContent(content, context = {}) {
        try {
            const response = await fetch(`${this.settings.apiEndpoint}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    context: {
                        ...context,
                        source: 'browser_extension',
                        timestamp: new Date().toISOString()
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
            
        } catch (error) {
            console.error('Analysis error:', error);
            throw error;
        }
    }
    
    async checkApiConnection() {
        try {
            const response = await fetch(`${this.settings.apiEndpoint}/api-info`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
    
    async getAnalysisHistory() {
        try {
            const result = await chrome.storage.sync.get(['analysisHistory']);
            return result.analysisHistory || [];
        } catch (error) {
            return [];
        }
    }
    
    async saveToHistory(analysis) {
        try {
            const history = await this.getAnalysisHistory();
            history.unshift({
                ...analysis,
                timestamp: new Date().toISOString()
            });
            
            // Keep only last 100 analyses
            const limitedHistory = history.slice(0, 100);
            
            await chrome.storage.sync.set({ analysisHistory: limitedHistory });
        } catch (error) {
            console.error('Error saving to history:', error);
        }
    }
    
    showNotification(message, type = 'info') {
        if (!this.settings.showNotifications) return;
        
        const notificationOptions = {
            type: 'basic',
            iconUrl: chrome.runtime.getURL('icons/icon48.png'),
            title: 'LRDEnE Guardian',
            message: message
        };
        
        // Set priority based on type
        if (type === 'error' || type === 'warning') {
            notificationOptions.requireInteraction = true;
        }
        
        chrome.notifications.create(notificationOptions);
    }
}

// Initialize background service worker
new GuardianBackground();
