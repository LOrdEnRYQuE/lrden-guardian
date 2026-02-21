// LRDEnE Guardian Options Script
class GuardianOptions {
    constructor() {
        this.settings = {};
        this.initializeElements();
        this.loadSettings();
        this.loadStatistics();
    }
    
    initializeElements() {
        this.elements = {
            apiEndpoint: document.getElementById('apiEndpoint'),
            autoAnalyze: document.getElementById('autoAnalyze'),
            showNotifications: document.getElementById('showNotifications'),
            realTimeProtection: document.getElementById('realTimeProtection'),
            newSite: document.getElementById('newSite'),
            sitesList: document.getElementById('sitesList'),
            statusMessage: document.getElementById('statusMessage'),
            totalAnalyses: document.getElementById('totalAnalyses'),
            safeAnalyses: document.getElementById('safeAnalyses'),
            riskAnalyses: document.getElementById('riskAnalyses'),
            avgGuardianScore: document.getElementById('avgGuardianScore')
        };
    }
    
    async loadSettings() {
        try {
            const response = await chrome.runtime.sendMessage({ action: 'getSettings' });
            if (response.success) {
                this.settings = response.settings;
                this.populateSettings();
            }
        } catch (error) {
            this.showStatus('Error loading settings: ' + error.message, 'error');
        }
    }
    
    populateSettings() {
        this.elements.apiEndpoint.value = this.settings.apiEndpoint || 'http://localhost:5001';
        this.elements.autoAnalyze.checked = this.settings.autoAnalyze !== false;
        this.elements.showNotifications.checked = this.settings.showNotifications !== false;
        this.elements.realTimeProtection.checked = this.settings.realTimeProtection === true;
        
        this.populateSitesList();
    }
    
    populateSitesList() {
        const sites = this.settings.protectedSites || [];
        this.elements.sitesList.innerHTML = '';
        
        sites.forEach((site, index) => {
            const siteTag = document.createElement('div');
            siteTag.className = 'site-tag';
            siteTag.innerHTML = `
                <span>${site}</span>
                <button onclick="guardianOptions.removeSite(${index})" title="Remove">×</button>
            `;
            this.elements.sitesList.appendChild(siteTag);
        });
    }
    
    async loadStatistics() {
        try {
            const response = await chrome.runtime.sendMessage({ action: 'getAnalysisHistory' });
            if (response.success) {
                this.updateStatistics(response.history);
            }
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }
    
    updateStatistics(history) {
        const total = history.length;
        const safe = history.filter(item => item.is_safe).length;
        const risk = total - safe;
        const avgScore = total > 0 ? 
            history.reduce((sum, item) => sum + (item.guardian_score || 0), 0) / total : 0;
        
        this.elements.totalAnalyses.textContent = total;
        this.elements.safeAnalyses.textContent = safe;
        this.elements.riskAnalyses.textContent = risk;
        this.elements.avgGuardianScore.textContent = avgScore.toFixed(3);
    }
    
    async saveSettings() {
        const newSettings = {
            apiEndpoint: this.elements.apiEndpoint.value.trim(),
            autoAnalyze: this.elements.autoAnalyze.checked,
            showNotifications: this.elements.showNotifications.checked,
            realTimeProtection: this.elements.realTimeProtection.checked,
            protectedSites: this.settings.protectedSites || []
        };
        
        // Validate API endpoint
        if (!newSettings.apiEndpoint) {
            this.showStatus('Please enter a valid API endpoint', 'error');
            return;
        }
        
        try {
            const response = await chrome.runtime.sendMessage({
                action: 'updateSettings',
                settings: newSettings
            });
            
            if (response.success) {
                this.settings = newSettings;
                this.showStatus('Settings saved successfully!', 'success');
            } else {
                this.showStatus('Error saving settings: ' + response.error, 'error');
            }
        } catch (error) {
            this.showStatus('Error saving settings: ' + error.message, 'error');
        }
    }
    
    async testConnection() {
        const endpoint = this.elements.apiEndpoint.value.trim();
        
        if (!endpoint) {
            this.showStatus('Please enter an API endpoint first', 'error');
            return;
        }
        
        this.showStatus('Testing connection...', 'info');
        
        try {
            const response = await fetch(`${endpoint}/api-info`);
            
            if (response.ok) {
                this.showStatus('Connection successful! LRDEnE Guardian is running.', 'success');
            } else {
                this.showStatus('Connection failed: Server returned error', 'error');
            }
        } catch (error) {
            this.showStatus('Connection failed: ' + error.message, 'error');
        }
    }
    
    addSite() {
        const site = this.elements.newSite.value.trim().toLowerCase();
        
        if (!site) {
            this.showStatus('Please enter a domain name', 'error');
            return;
        }
        
        // Validate domain format
        if (!this.isValidDomain(site)) {
            this.showStatus('Please enter a valid domain (e.g., twitter.com)', 'error');
            return;
        }
        
        // Check for duplicates
        const sites = this.settings.protectedSites || [];
        if (sites.includes(site)) {
            this.showStatus('This site is already in the list', 'error');
            return;
        }
        
        // Add site
        sites.push(site);
        this.settings.protectedSites = sites;
        
        // Update UI
        this.populateSitesList();
        this.elements.newSite.value = '';
        
        this.showStatus(`Added ${site} to protected sites`, 'success');
    }
    
    removeSite(index) {
        const sites = this.settings.protectedSites || [];
        const removedSite = sites[index];
        
        sites.splice(index, 1);
        this.settings.protectedSites = sites;
        
        this.populateSitesList();
        this.showStatus(`Removed ${removedSite} from protected sites`, 'success');
    }
    
    isValidDomain(domain) {
        // Simple domain validation
        const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9])*$/;
        return domainRegex.test(domain) && domain.length <= 255;
    }
    
    async clearHistory() {
        if (!confirm('Are you sure you want to clear all analysis history? This action cannot be undone.')) {
            return;
        }
        
        try {
            await chrome.storage.sync.set({ analysisHistory: [] });
            this.updateStatistics([]);
            this.showStatus('History cleared successfully', 'success');
        } catch (error) {
            this.showStatus('Error clearing history: ' + error.message, 'error');
        }
    }
    
    showStatus(message, type) {
        const statusElement = this.elements.statusMessage;
        statusElement.textContent = message;
        statusElement.className = `status ${type}`;
        statusElement.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 5000);
    }
}

// Initialize options page
const guardianOptions = new GuardianOptions();

// Make functions globally accessible for inline event handlers
window.guardianOptions = guardianOptions;
