// LRDEnE Guardian Enhanced UI/UX JavaScript
// Enhanced user experience with modern interactions and animations

class EnhancedUI {
    constructor() {
        this.initializeComponents();
        this.attachEventListeners();
        this.initializeCharts();
        this.loadAnalytics();
    }

    initializeComponents() {
        // Initialize theme toggle
        this.themeToggle = document.getElementById('themeToggle');
        this.themeIcon = document.getElementById('themeIcon');
        this.mobileMenuToggle = document.getElementById('mobileMenuToggle');
        this.mobileMenu = document.getElementById('mobileMenu');
        
        // Initialize analysis components
        this.contentInput = document.getElementById('contentInput');
        this.charCount = document.getElementById('charCount');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.demoBtn = document.getElementById('demoBtn');
        this.clearText = document.getElementById('clearText');
        
        // Initialize file upload
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.browseBtn = document.getElementById('browseBtn');
        this.fileList = document.getElementById('fileList');
        
        // Initialize URL analysis
        this.urlInput = document.getElementById('urlInput');
        this.analyzeUrlBtn = document.getElementById('analyzeUrlBtn');
        
        // Initialize tabs
        this.tabButtons = document.querySelectorAll('.tab-btn');
        this.tabPanes = document.querySelectorAll('.tab-pane');
        
        // Initialize results
        this.resultsSection = document.getElementById('resultsSection');
        this.analysisResults = document.getElementById('analysisResults');
        
        // Initialize loading states
        this.loadingStates = {
            analyze: false,
            file: false,
            url: false
        };
        
        // Initialize analytics
        this.charts = {};
        this.analyticsData = {
            total: 0,
            safe: 0,
            risk: 0,
            scores: [],
            timestamps: []
        };
    }

    attachEventListeners() {
        // Theme toggle
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
        
        // Mobile menu
        if (this.mobileMenuToggle && this.mobileMenu) {
            this.mobileMenuToggle.addEventListener('click', () => this.toggleMobileMenu());
        }
        
        // Tab navigation
        this.tabButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Text input events
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
        
        if (this.demoBtn) {
            this.demoBtn.addEventListener('click', () => this.loadDemoContent());
        }
        
        if (this.clearText) {
            this.clearText.addEventListener('click', () => this.clearContent());
        }
        
        // File upload events
        if (this.dropZone) {
            this.setupFileUpload();
        }
        
        if (this.browseBtn) {
            this.browseBtn.addEventListener('click', () => this.fileInput.click());
        }
        
        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
        
        // URL analysis events
        if (this.analyzeUrlBtn) {
            this.analyzeUrlBtn.addEventListener('click', () => this.analyzeUrl());
        }
        
        if (this.urlInput) {
            this.urlInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.analyzeUrl();
                }
            });
        }
        
        // Example URLs
        document.querySelectorAll('.example-url').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.urlInput.value = e.target.dataset.url;
                this.analyzeUrl();
            });
        });
        
        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
        
        // Enhanced form validation
        this.setupFormValidation();
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        // Auto-save functionality
        this.setupAutoSave();
    }

    toggleTheme() {
        const html = document.documentElement;
        const isDark = html.classList.contains('dark');
        
        if (isDark) {
            html.classList.remove('dark');
            this.themeIcon.className = 'ri-sun-line text-gray-700';
            localStorage.setItem('theme', 'light');
        } else {
            html.classList.add('dark');
            this.themeIcon.className = 'ri-moon-line text-gray-700';
            localStorage.setItem('theme', 'dark');
        }
        
        // Update charts for theme
        this.updateChartsTheme();
    }

    toggleMobileMenu() {
        this.mobileMenu.classList.toggle('hidden');
        
        // Animate menu items
        if (!this.mobileMenu.classList.contains('hidden')) {
            const items = this.mobileMenu.querySelectorAll('a');
            items.forEach((item, index) => {
                item.style.opacity = '0';
                item.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    item.style.transition = 'all 0.3s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, index * 50);
            });
        }
    }

    switchTab(tabName) {
        // Update button states
        this.tabButtons.forEach(btn => {
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active', 'text-purple-600', 'border-b-2', 'border-purple-600');
                btn.classList.remove('text-gray-500');
            } else {
                btn.classList.remove('active', 'text-purple-600', 'border-b-2', 'border-purple-600');
                btn.classList.add('text-gray-500');
            }
        });
        
        // Update pane visibility with animation
        this.tabPanes.forEach(pane => {
            if (pane.id === `${tabName}Tab`) {
                pane.classList.remove('hidden');
                pane.classList.add('fade-in');
            } else {
                pane.classList.add('hidden');
                pane.classList.remove('fade-in');
            }
        });
    }

    updateCharCount() {
        const count = this.contentInput.value.length;
        this.charCount.textContent = count;
        
        // Update character count color
        if (count > 9000) {
            this.charCount.classList.add('text-red-500');
            this.charCount.classList.remove('text-gray-500');
        } else {
            this.charCount.classList.remove('text-red-500');
            this.charCount.classList.add('text-gray-500');
        }
        
        // Enable/disable analyze button
        this.analyzeBtn.disabled = count < 10;
    }

    clearContent() {
        this.contentInput.value = '';
        this.updateCharCount();
        this.contentInput.focus();
        
        // Add clear animation
        this.contentInput.classList.add('scale-in');
        setTimeout(() => {
            this.contentInput.classList.remove('scale-in');
        }, 300);
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
        
        this.setLoadingState('analyze', true);
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    context: {
                        source: 'enhanced_web_dashboard',
                        timestamp: new Date().toISOString(),
                        user_agent: navigator.userAgent
                    }
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.displayResults(result);
                this.updateAnalytics(result);
                this.saveToHistory(result, 'text');
            } else {
                throw new Error(result.error || 'Analysis failed');
            }
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            this.setLoadingState('analyze', false);
        }
    }

    setupFileUpload() {
        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
            this.dropZone.addEventListener(event, (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                if (event.type === 'dragenter' || event.type === 'dragover') {
                    this.dropZone.classList.add('border-purple-400', 'bg-purple-50');
                } else {
                    this.dropZone.classList.remove('border-purple-400', 'bg-purple-50');
                }
            });
        });
        
        this.dropZone.addEventListener('drop', (e) => {
            const files = Array.from(e.dataTransfer.files);
            this.handleFiles(files);
        });
        
        // Click to upload
        this.dropZone.addEventListener('click', () => {
            this.fileInput.click();
        });
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.handleFiles(files);
    }

    handleFiles(files) {
        if (files.length === 0) return;
        
        // Validate files
        const validFiles = files.filter(file => {
            const validTypes = ['text/plain', 'text/markdown', 'application/pdf', 
                              'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            const maxSize = 10 * 1024 * 1024; // 10MB
            
            return validTypes.includes(file.type) && file.size <= maxSize;
        });
        
        if (validFiles.length === 0) {
            this.showNotification('Please select valid files (TXT, MD, PDF, DOC, DOCX) under 10MB', 'warning');
            return;
        }
        
        if (validFiles.length < files.length) {
            this.showNotification(`${files.length - validFiles.length} files were invalid and skipped`, 'info');
        }
        
        // Display file list
        this.displayFileList(validFiles);
        
        // Process files
        this.processFiles(validFiles);
    }

    displayFileList(files) {
        this.fileList.innerHTML = '';
        
        files.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'flex items-center justify-between p-4 bg-gray-50 rounded-lg fade-in';
            fileItem.innerHTML = `
                <div class="flex items-center space-x-3">
                    <i class="ri-file-text-line text-purple-600 text-xl"></i>
                    <div>
                        <div class="font-medium text-gray-900">${file.name}</div>
                        <div class="text-sm text-gray-500">${this.formatFileSize(file.size)}</div>
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="status-badge status-info">Ready</span>
                    <button class="text-red-500 hover:text-red-700 transition-colors" onclick="enhancedUI.removeFile(${index})">
                        <i class="ri-close-circle-line"></i>
                    </button>
                </div>
            `;
            this.fileList.appendChild(fileItem);
        });
    }

    removeFile(index) {
        const fileItems = this.fileList.children;
        if (fileItems[index]) {
            fileItems[index].classList.add('fade-out');
            setTimeout(() => {
                fileItems[index].remove();
            }, 300);
        }
    }

    async processFiles(files) {
        this.setLoadingState('file', true);
        
        for (const file of files) {
            try {
                const content = await this.readFile(file);
                const result = await this.analyzeFileContent(content, file.name);
                this.displayResults(result);
                this.updateAnalytics(result);
                this.saveToHistory(result, 'file', file.name);
            } catch (error) {
                console.error('File processing error:', error);
                this.showNotification(`Error processing ${file.name}: ${error.message}`, 'error');
            }
        }
        
        this.setLoadingState('file', false);
    }

    readFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(new Error('File reading failed'));
            reader.readAsText(file);
        });
    }

    async analyzeFileContent(content, filename) {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: content,
                context: {
                    source: 'file_upload',
                    filename: filename,
                    timestamp: new Date().toISOString()
                }
            })
        });
        
        return await response.json();
    }

    async analyzeUrl() {
        const url = this.urlInput.value.trim();
        
        if (!url) {
            this.showNotification('Please enter a URL to analyze', 'warning');
            return;
        }
        
        if (!this.isValidUrl(url)) {
            this.showNotification('Please enter a valid URL', 'warning');
            return;
        }
        
        this.setLoadingState('url', true);
        
        try {
            // First fetch the URL content
            const content = await this.fetchUrlContent(url);
            
            // Then analyze the content
            const result = await this.analyzeFileContent(content, url);
            this.displayResults(result);
            this.updateAnalytics(result);
            this.saveToHistory(result, 'url', url);
            
        } catch (error) {
            console.error('URL analysis error:', error);
            this.showNotification('URL analysis failed: ' + error.message, 'error');
        } finally {
            this.setLoadingState('url', false);
        }
    }

    async fetchUrlContent(url) {
        // In a real implementation, this would use a proxy server
        // For demo purposes, we'll simulate URL content
        return `Content from ${url}\n\nThis is sample content for demonstration purposes. In a real implementation, this would fetch the actual content from the URL.`;
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch {
            return false;
        }
    }

    displayResults(result) {
        this.resultsSection.classList.remove('hidden');
        
        const riskClass = result.is_safe ? 'safe' : result.risk_level === 'high' ? 'danger' : 'warning';
        const statusIcon = result.is_safe ? '✅' : '⚠️';
        const statusText = result.is_safe ? 'Safe Content' : 'Requires Review';
        
        const resultHtml = `
            <div class="analysis-result ${riskClass} fade-in">
                <div class="flex items-center justify-between mb-6">
                    <div class="flex items-center space-x-3">
                        <div class="text-2xl">${statusIcon}</div>
                        <div>
                            <h5 class="text-lg font-semibold">${statusText}</h5>
                            <p class="text-sm opacity-75">Risk Level: ${result.risk_level?.toUpperCase() || 'UNKNOWN'}</p>
                        </div>
                    </div>
                    <div class="guardian-score" data-score="${result.guardian_score?.toFixed(3) || '0.000'}"></div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div class="text-center">
                        <div class="text-2xl font-bold text-gray-700">${(result.confidence_score * 100).toFixed(1)}%</div>
                        <div class="text-sm text-gray-500">Confidence</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold text-purple-600">${result.guardian_score?.toFixed(3) || '0.000'}</div>
                        <div class="text-sm text-gray-500">Guardian Score</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold ${result.is_safe ? 'text-green-600' : 'text-yellow-600'}">
                            ${result.is_safe ? '✓' : '!'}
                        </div>
                        <div class="text-sm text-gray-500">Safety Status</div>
                    </div>
                </div>
                
                ${result.analysis_summary ? `
                <div class="mb-6">
                    <h6 class="text-lg font-semibold text-gray-700 mb-3">Summary</h6>
                    <p class="text-gray-600">${result.analysis_summary}</p>
                </div>
                ` : ''}
                
                ${result.detected_issues && result.detected_issues.length > 0 ? `
                <div class="mb-6">
                    <h6 class="text-lg font-semibold text-red-700 mb-3">
                        <i class="ri-alert-line mr-2"></i>Detected Issues
                    </h6>
                    <ul class="space-y-2">
                        ${result.detected_issues.map(issue => `
                            <li class="flex items-start space-x-2">
                                <i class="ri-checkbox-circle-fill text-red-500 mt-0.5"></i>
                                <span class="text-gray-700">${issue}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
                ` : ''}
                
                ${result.recommendations && result.recommendations.length > 0 ? `
                <div class="mb-6">
                    <h6 class="text-lg font-semibold text-blue-700 mb-3">
                        <i class="ri-lightbulb-line mr-2"></i>Recommendations
                    </h6>
                    <ul class="space-y-2">
                        ${result.recommendations.map(rec => `
                            <li class="flex items-start space-x-2">
                                <i class="ri-arrow-right-line text-blue-500 mt-0.5"></i>
                                <span class="text-gray-700">${rec}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
                ` : ''}
                
                <div class="flex items-center justify-between pt-6 border-t border-gray-200">
                    <div class="text-sm text-gray-500">
                        Analyzed at ${new Date(result.timestamp || Date.now()).toLocaleString()}
                    </div>
                    <div class="flex space-x-2">
                        <button onclick="enhancedUI.shareResults()" class="btn btn-secondary text-sm">
                            <i class="ri-share-line mr-1"></i>Share
                        </button>
                        <button onclick="enhancedUI.exportResults()" class="btn btn-secondary text-sm">
                            <i class="ri-download-line mr-1"></i>Export
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        this.analysisResults.innerHTML = resultHtml;
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Add entrance animation
        setTimeout(() => {
            const resultElement = this.analysisResults.querySelector('.analysis-result');
            if (resultElement) {
                resultElement.classList.add('scale-in');
            }
        }, 100);
    }

    setLoadingState(type, loading) {
        this.loadingStates[type] = loading;
        
        // Update button states
        if (type === 'analyze') {
            this.analyzeBtn.disabled = loading;
            if (loading) {
                this.analyzeBtn.innerHTML = '<i class="ri-loader-4-line animate-spin mr-2"></i>Analyzing...';
            } else {
                this.analyzeBtn.innerHTML = '<i class="ri-search-line mr-2"></i>Analyze Content';
            }
        }
        
        if (type === 'file') {
            this.browseBtn.disabled = loading;
            if (loading) {
                this.browseBtn.innerHTML = '<i class="ri-loader-4-line animate-spin mr-2"></i>Processing...';
            } else {
                this.browseBtn.innerHTML = 'Choose Files';
            }
        }
        
        if (type === 'url') {
            this.analyzeUrlBtn.disabled = loading;
            if (loading) {
                this.analyzeUrlBtn.innerHTML = '<i class="ri-loader-4-line animate-spin mr-2"></i>Analyzing...';
            } else {
                this.analyzeUrlBtn.innerHTML = '<i class="ri-search-line mr-2"></i>Analyze URL';
            }
        }
    }

    loadDemoContent() {
        const demoContent = `As an AI language model, I can provide you with comprehensive information about various topics. However, I must clarify that while I strive to be accurate, I may occasionally generate responses that contain inaccuracies or "hallucinations" - statements that appear factual but are not actually correct.

I have access to a vast amount of training data, but my knowledge has a cutoff date, so I may not have information about very recent events. Additionally, I cannot browse the internet in real-time or access proprietary databases.

For the most accurate and up-to-date information, I recommend verifying critical information through primary sources, academic journals, or official documentation. This is especially important for medical, legal, financial, or safety-critical information.

Remember to use AI assistance as a helpful tool rather than as an infallible source of truth. Critical thinking and fact-checking remain essential skills when working with AI-generated content.`;
        
        this.contentInput.value = demoContent;
        this.updateCharCount();
        
        // Add typing animation
        this.contentInput.classList.add('fade-in');
        setTimeout(() => {
            this.contentInput.classList.remove('fade-in');
        }, 100);
        
        this.showNotification('Demo content loaded. This contains AI indicators for testing.', 'info');
    }

    initializeCharts() {
        // Risk Distribution Chart
        const riskCtx = document.getElementById('riskChart');
        if (riskCtx) {
            this.charts.risk = new Chart(riskCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Safe', 'Low Risk', 'Medium Risk', 'High Risk'],
                    datasets: [{
                        data: [0, 0, 0, 0],
                        backgroundColor: [
                            '#10b981',
                            '#f59e0b',
                            '#f97316',
                            '#ef4444'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                });
        }
        
        // Trends Chart
        const trendsCtx = document.getElementById('trendsChart');
        if (trendsCtx) {
            this.charts.trends = new Chart(trendsCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Guardian Scores',
                        data: [],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
    }

    updateChartsTheme() {
        const isDark = document.documentElement.classList.contains('dark');
        const textColor = isDark ? '#f1f5f9' : '#374151';
        const gridColor = isDark ? '#374151' : '#e5e7eb';
        
        // Update risk chart
        if (this.charts.risk) {
            this.charts.risk.options.plugins.legend.labels.color = textColor;
            this.charts.risk.update();
        }
        
        // Update trends chart
        if (this.charts.trends) {
            this.charts.trends.options.scales.x.ticks.color = textColor;
            this.charts.trends.options.scales.y.ticks.color = textColor;
            this.charts.trends.options.scales.x.grid.color = gridColor;
            this.charts.trends.options.scales.y.grid.color = gridColor;
            this.charts.trends.update();
        }
    }

    updateAnalytics(result) {
        this.analyticsData.total++;
        
        if (result.is_safe) {
            this.analyticsData.safe++;
        } else {
            this.analyticsData.risk++;
        }
        
        if (result.guardian_score) {
            this.analyticsData.scores.push(result.guardian_score);
            this.analyticsData.timestamps.push(new Date());
        }
        
        // Keep only last 100 scores
        if (this.analyticsData.scores.length > 100) {
            this.analyticsData.scores.shift();
            this.analyticsData.timestamps.shift();
        }
        
        this.updateAnalyticsDisplay();
        this.updateCharts();
    }

    updateAnalyticsDisplay() {
        // Update overview stats
        const totalEl = document.getElementById('totalAnalyses');
        const safeEl = document.getElementById('safeAnalyses');
        const riskEl = document.getElementById('riskAnalyses');
        const avgScoreEl = document.getElementById('avgScore');
        
        if (totalEl) totalEl.textContent = this.analyticsData.total;
        if (safeEl) safeEl.textContent = this.analyticsData.safe;
        if (riskEl) riskEl.textContent = this.analyticsData.risk;
        
        if (avgScoreEl && this.analyticsData.scores.length > 0) {
            const avgScore = this.analyticsData.scores.reduce((a, b) => a + b, 0) / this.analyticsData.scores.length;
            avgScoreEl.textContent = avgScore.toFixed(3);
        }
        
        // Update recent activity
        this.updateRecentActivity();
    }

    updateCharts() {
        // Update risk distribution
        if (this.charts.risk) {
            const riskData = [
                this.analyticsData.safe,
                this.analyticsData.risk - this.analyticsData.highRisk || 0,
                this.analyticsData.mediumRisk || 0,
                this.analyticsData.highRisk || 0
            ];
            this.charts.risk.data.datasets[0].data = riskData;
            this.charts.risk.update();
        }
        
        // Update trends chart
        if (this.charts.trends && this.analyticsData.scores.length > 0) {
            const labels = this.analyticsData.timestamps.map(ts => 
                ts.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            );
            this.charts.trends.data.labels = labels;
            this.charts.trends.data.datasets[0].data = this.analyticsData.scores;
            this.charts.trends.update();
        }
    }

    updateRecentActivity() {
        const recentActivity = document.getElementById('recentActivity');
        if (!recentActivity) return;
        
        // Get last 5 activities from local storage
        const activities = JSON.parse(localStorage.getItem('lrden_activities') || '[]');
        const recent = activities.slice(-5).reverse();
        
        if (recent.length === 0) {
            recentActivity.innerHTML = '<p class="text-gray-500 text-center">No recent activity</p>';
            return;
        }
        
        recentActivity.innerHTML = recent.map(activity => `
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div class="flex items-center space-x-3">
                    <i class="${activity.type === 'text' ? 'ri-text' : activity.type === 'file' ? 'ri-file-text' : 'ri-link'} text-purple-600"></i>
                    <div>
                        <div class="text-sm font-medium text-gray-900">${activity.title}</div>
                        <div class="text-xs text-gray-500">${activity.timestamp}</div>
                    </div>
                </div>
                <span class="status-badge status-${activity.status}">${activity.status}</span>
            </div>
        `).join('');
    }

    saveToHistory(result, type, title) {
        const activities = JSON.parse(localStorage.getItem('lrden_activities') || '[]');
        
        const activity = {
            type: type,
            title: title || `${type.substring(0, 1).toUpperCase()}${type.substring(1)} Analysis`,
            status: result.is_safe ? 'safe' : result.risk_level || 'warning',
            score: result.guardian_score,
            timestamp: new Date().toLocaleString(),
            result: result
        };
        
        activities.push(activity);
        
        // Keep only last 50 activities
        if (activities.length > 50) {
            activities.shift();
        }
        
        localStorage.setItem('lrden_activities', JSON.stringify(activities));
    }

    loadAnalytics() {
        // Load saved analytics from localStorage
        const saved = localStorage.getItem('lrden_analytics');
        if (saved) {
            this.analyticsData = JSON.parse(saved);
            this.updateAnalyticsDisplay();
            this.updateCharts();
        }
    }

    saveAnalytics() {
        localStorage.setItem('lrden_analytics', JSON.stringify(this.analyticsData));
    }

    setupFormValidation() {
        // Enhanced form validation with real-time feedback
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => this.clearFieldError(input));
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';
        
        // Email validation
        if (field.type === 'email') {
            isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
            message = 'Please enter a valid email address';
        }
        
        // URL validation
        if (field.type === 'url') {
            try {
                new URL(value);
                isValid = value.length > 0;
                message = 'Please enter a valid URL';
            } catch {
                isValid = false;
                message = 'Please enter a valid URL';
            }
        }
        
        // Required field validation
        if (field.required && !value) {
            isValid = false;
            message = 'This field is required';
        }
        
        // Length validation
        if (field.minLength && value.length < field.minLength) {
            isValid = false;
            message = `Minimum length is ${field.minLength} characters`;
        }
        
        // Show validation feedback
        if (!isValid) {
            this.showFieldError(field, message);
        } else {
            this.clearFieldError(field);
        }
        
        return isValid;
    }

    showFieldError(field, message) {
        field.classList.add('border-red-500');
        
        // Remove existing error message
        this.clearFieldError(field);
        
        // Add error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-red-500 text-sm mt-1 fade-in';
        errorDiv.textContent = message;
        errorDiv.setAttribute('role', 'alert');
        
        field.parentNode.appendChild(errorDiv);
    }

    clearFieldError(field) {
        field.classList.remove('border-red-500');
        const errorDiv = field.parentNode.querySelector('.text-red-500');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K: Clear content
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                if (this.contentInput === document.activeElement) {
                    this.clearContent();
                }
            }
            
            // Ctrl/Cmd + Enter: Analyze content
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                if (this.contentInput === document.activeElement) {
                    this.analyzeContent();
                }
            }
            
            // Ctrl/Cmd + D: Load demo
            if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                e.preventDefault();
                this.loadDemoContent();
            }
            
            // Escape: Clear results
            if (e.key === 'Escape') {
                this.resultsSection.classList.add('hidden');
            }
        });
    }

    setupAutoSave() {
        // Auto-save content to localStorage
        if (this.contentInput) {
            let saveTimeout;
            
            this.contentInput.addEventListener('input', () => {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    localStorage.setItem('lrden_draft_content', this.contentInput.value);
                }, 1000);
            });
            
            // Load draft on page load
            const draft = localStorage.getItem('lrden_draft_content');
            if (draft && !this.contentInput.value) {
                this.contentInput.value = draft;
                this.updateCharCount();
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
                <i class="ri-${type === 'info' ? 'information' : type === 'success' ? 'checkbox-circle' : type === 'warning' ? 'alert' : 'error'}-line"></i>
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
                url: window.location.href
            });
        } else {
            // Fallback: copy to clipboard
            this.copyToClipboard(window.location.href);
            this.showNotification('Link copied to clipboard', 'success');
        }
    }

    exportResults() {
        // Implement export functionality
        const results = this.analysisResults.textContent;
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
            // Success feedback
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Initialize the enhanced UI
    static init() {
        window.enhancedUI = new EnhancedUI();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    EnhancedUI.init();
});

// Make it globally available
window.EnhancedUI = EnhancedUI;
