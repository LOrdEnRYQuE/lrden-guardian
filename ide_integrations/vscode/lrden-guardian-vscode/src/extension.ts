import * as vscode from 'vscode';
import axios from 'axios';
import { debounce } from 'debounce';

interface GuardianAnalysis {
    is_safe: boolean;
    risk_level: string;
    confidence_score: number;
    guardian_score: number;
    analysis_summary: string;
    recommendations: string[];
    detected_issues: string[];
    uncertainty_areas: string[];
    timestamp: string;
}

interface GuardianConfig {
    apiEndpoint: string;
    autoAnalysis: boolean;
    analysisDelay: number;
    showDecorations: boolean;
    showNotifications: boolean;
    riskThreshold: string;
    supportedLanguages: string[];
}

class LRDEnEGuardianExtension {
    private config: GuardianConfig;
    private analysisCache: Map<string, GuardianAnalysis> = new Map();
    private decorationTypes: vscode.TextEditorDecorationType[] = [];
    private outputChannel: vscode.OutputChannel;
    private statusBarItem: vscode.StatusBarItem;
    public analysisProvider: AnalysisProvider;

    constructor() {
        this.config = this.loadConfiguration();
        this.outputChannel = vscode.window.createOutputChannel('LRDEnE Guardian');
        this.statusBarItem = vscode.window.createStatusBarItem('lrden-guardian-status', vscode.StatusBarAlignment.Right, 100);
        this.analysisProvider = new AnalysisProvider();
        
        this.initializeDecorations();
        this.registerCommands();
        this.registerEventListeners();
        this.updateStatusBar();
    }

    private loadConfiguration(): GuardianConfig {
        const config = vscode.workspace.getConfiguration('lrdenGuardian');
        return {
            apiEndpoint: config.get('apiEndpoint', 'http://localhost:5001'),
            autoAnalysis: config.get('autoAnalysis', true),
            analysisDelay: config.get('analysisDelay', 1000),
            showDecorations: config.get('showDecorations', true),
            showNotifications: config.get('showNotifications', true),
            riskThreshold: config.get('riskThreshold', 'medium'),
            supportedLanguages: config.get('supportedLanguages', ['python', 'javascript', 'typescript', 'java', 'cpp', 'c', 'go', 'rust', 'php', 'ruby', 'markdown'])
        };
    }

    private initializeDecorations() {
        // Safe content decoration
        this.decorationTypes.push(vscode.window.createTextEditorDecorationType({
            backgroundColor: 'rgba(17, 153, 142, 0.1)',
            border: '2px solid #11998e',
            borderRadius: '3px',
            isWholeLine: false
        }));

        // Warning decoration
        this.decorationTypes.push(vscode.window.createTextEditorDecorationType({
            backgroundColor: 'rgba(252, 74, 26, 0.1)',
            border: '2px solid #fc4a1a',
            borderRadius: '3px',
            isWholeLine: false
        }));

        // Danger decoration
        this.decorationTypes.push(vscode.window.createTextEditorDecorationType({
            backgroundColor: 'rgba(235, 51, 73, 0.1)',
            border: '2px solid #eb3349',
            borderRadius: '3px',
            isWholeLine: false
        }));
    }

    public registerCommands() {
        const commands = [
            vscode.commands.registerCommand('lrdenGuardian.analyzeSelection', () => this.analyzeSelection()),
            vscode.commands.registerCommand('lrdenGuardian.analyzeFile', () => this.analyzeFile()),
            vscode.commands.registerCommand('lrdenGuardian.analyzeProject', () => this.analyzeProject()),
            vscode.commands.registerCommand('lrdenGuardian.toggleAutoAnalysis', () => this.toggleAutoAnalysis()),
            vscode.commands.registerCommand('lrdenGuardian.showSettings', () => this.showSettings()),
            vscode.commands.registerCommand('lrdenGuardian.showDashboard', () => this.showDashboard())
        ];

        return commands;
    }

    private registerEventListeners() {
        // Configuration change listener
        vscode.workspace.onDidChangeConfiguration(() => {
            this.config = this.loadConfiguration();
            this.updateStatusBar();
        });

        // Text change listener for auto-analysis
        if (this.config.autoAnalysis) {
            const debouncedAnalysis = debounce((editor: vscode.TextEditor, changes: vscode.TextDocumentContentChangeEvent[]) => {
                this.handleTextChange(editor, changes);
            }, this.config.analysisDelay);

            vscode.workspace.onDidChangeTextDocument((event) => {
                const editor = vscode.window.activeTextEditor;
                if (editor && editor.document === event.document) {
                    debouncedAnalysis(editor, event.contentChanges);
                }
            });
        }
    }

    private async analyzeSelection() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor found');
            return;
        }

        const selection = editor.selection;
        if (selection.isEmpty) {
            vscode.window.showWarningMessage('No text selected');
            return;
        }

        const selectedText = editor.document.getText(selection);
        if (selectedText.trim().length < 10) {
            vscode.window.showWarningMessage('Selection too short for analysis');
            return;
        }

        await this.performAnalysis(selectedText, 'selection', editor);
    }

    private async analyzeFile() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor found');
            return;
        }

        const content = editor.document.getText();
        if (content.trim().length < 10) {
            vscode.window.showWarningMessage('File too short for analysis');
            return;
        }

        await this.performAnalysis(content, 'file', editor);
    }

    private async analyzeProject() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showWarningMessage('No workspace folder found');
            return;
        }

        const progress = vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Analyzing Project',
            cancellable: true
        }, async (progress, token) => {
            progress.report({ increment: 0, message: 'Starting project analysis...' });

            const files = await vscode.workspace.findFiles('**/*.{py,js,ts,java,cpp,c,go,rust,php,rb,md}', '**/node_modules/**');
            const totalFiles = files.length;
            let analyzedFiles = 0;
            let riskyFiles = 0;

            for (const file of files.slice(0, 50)) { // Limit to 50 files for performance
                if (token.isCancellationRequested) {
                    break;
                }

                progress.report({ 
                    increment: (analyzedFiles / totalFiles) * 100, 
                    message: `Analyzing ${file.fsPath}...` 
                });

                try {
                    const content = await vscode.workspace.fs.readFile(file);
                    const analysis = await this.callGuardianAPI(content.toString(), {
                        source: 'vscode_project_analysis',
                        file_path: file.fsPath,
                        workspace: workspaceFolders[0].name
                    });

                    if (analysis && !analysis.is_safe) {
                        riskyFiles++;
                    }

                    analyzedFiles++;
                } catch (error) {
                    this.outputChannel.appendLine(`Error analyzing ${file.fsPath}: ${error}`);
                }
            }

            progress.report({ increment: 100, message: 'Analysis complete!' });

            const message = `Project analysis complete!\n\nTotal files analyzed: ${analyzedFiles}\nFiles with risks: ${riskyFiles}\n\n${riskyFiles > 0 ? '⚠️ Some files contain potential risks. Check the Analysis Results panel for details.' : '✅ No significant risks detected.'}`;
            vscode.window.showInformationMessage(message);
        });
    }

    private async handleTextChange(editor: vscode.TextEditor, changes: vscode.TextDocumentContentChangeEvent[]) {
        if (!this.config.autoAnalysis || !this.shouldAnalyzeLanguage(editor.document.languageId)) {
            return;
        }

        // Only analyze significant changes
        const significantChanges = changes.filter(change => change.text.length > 20);
        if (significantChanges.length === 0) {
            return;
        }

        // Get the changed text
        const changedText = significantChanges.map(change => change.text).join(' ');
        if (changedText.trim().length < 10) {
            return;
        }

        await this.performAnalysis(changedText, 'auto', editor);
    }

    private async performAnalysis(content: string, source: string, editor?: vscode.TextEditor) {
        try {
            this.updateStatusBar('Analyzing...', 'processing');
            
            const analysis = await this.callGuardianAPI(content, {
                source: `vscode_${source}`,
                file_path: editor?.document.fileName,
                language: editor?.document.languageId,
                workspace: vscode.workspace.name
            });

            if (analysis) {
                this.handleAnalysisResult(analysis, editor);
                this.analysisProvider.addAnalysis(analysis);
                
                if (this.config.showNotifications && !analysis.is_safe) {
                    vscode.window.showWarningMessage(
                        `⚠️ LRDEnE Guardian detected risks (${analysis.risk_level.toUpperCase()}): ${analysis.detected_issues[0] || 'Unknown issue'}`,
                        'View Details'
                    ).then(selection => {
                        if (selection === 'View Details') {
                            this.showAnalysisDetails(analysis);
                        }
                    });
                }
            }
        } catch (error) {
            this.outputChannel.appendLine(`Analysis error: ${error}`);
            vscode.window.showErrorMessage(`Analysis failed: ${error}`);
        } finally {
            this.updateStatusBar();
        }
    }

    private async callGuardianAPI(content: string, context: any): Promise<GuardianAnalysis | null> {
        try {
            const cacheKey = `${content.substring(0, 100)}_${JSON.stringify(context)}`;
            if (this.analysisCache.has(cacheKey)) {
                return this.analysisCache.get(cacheKey) || null;
            }

            const response = await axios.post(`${this.config.apiEndpoint}/analyze`, {
                content: content,
                context: {
                    ...context,
                    timestamp: new Date().toISOString()
                }
            }, {
                timeout: 10000,
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 200) {
                const analysis = response.data;
                
                // Cache the result
                this.analysisCache.set(cacheKey, analysis);
                
                // Limit cache size
                if (this.analysisCache.size > 1000) {
                    const firstKey = this.analysisCache.keys().next().value;
                    if (firstKey) {
                        this.analysisCache.delete(firstKey);
                    }
                }
                
                return analysis;
            }
        } catch (error) {
            this.outputChannel.appendLine(`API error: ${error}`);
            throw error;
        }

        return null;
    }

    private handleAnalysisResult(analysis: GuardianAnalysis, editor?: vscode.TextEditor) {
        if (!editor || !this.config.showDecorations) {
            return;
        }

        // Clear existing decorations
        editor.setDecorations(this.decorationTypes[0], []);
        editor.setDecorations(this.decorationTypes[1], []);
        editor.setDecorations(this.decorationTypes[2], []);

        // Apply new decorations based on risk level
        let decorationType: vscode.TextEditorDecorationType;
        let message: string;

        if (analysis.is_safe) {
            decorationType = this.decorationTypes[0];
            message = '✅ Safe content';
        } else {
            const riskLevels: { [key: string]: number } = { 'low': 1, 'medium': 2, 'high': 2, 'critical': 2 };
            const decorationIndex = riskLevels[analysis.risk_level] || 2;
            decorationType = this.decorationTypes[decorationIndex];
            message = `⚠️ ${analysis.risk_level.toUpperCase()} risk detected`;
        }

        // Apply decoration to entire document (you could make this more sophisticated)
        const fullRange = new vscode.Range(
            editor.document.positionAt(0),
            editor.document.positionAt(editor.document.getText().length)
        );
        
        editor.setDecorations(decorationType, [fullRange]);

        // Update status bar
        this.updateStatusBar(message, analysis.is_safe ? 'safe' : 'warning');
    }

    private shouldAnalyzeLanguage(languageId: string): boolean {
        return this.config.supportedLanguages.includes(languageId);
    }

    private toggleAutoAnalysis() {
        const newValue = !this.config.autoAnalysis;
        vscode.workspace.getConfiguration('lrdenGuardian').update('autoAnalysis', newValue);
        vscode.window.showInformationMessage(`Auto-analysis ${newValue ? 'enabled' : 'disabled'}`);
    }

    private showSettings() {
        vscode.commands.executeCommand('workbench.action.openSettings', '@ext:lrden-guardian-vscode');
    }

    private async showDashboard() {
        try {
            const response = await axios.get(`${this.config.apiEndpoint}/api-info`);
            if (response.status === 200) {
                const dashboardUrl = this.config.apiEndpoint.replace('/api-info', '');
                vscode.env.openExternal(vscode.Uri.parse(dashboardUrl));
            }
        } catch (error) {
            vscode.window.showErrorMessage('Unable to open dashboard. Make sure LRDEnE Guardian is running.');
        }
    }

    private showAnalysisDetails(analysis: GuardianAnalysis) {
        const panel = vscode.window.createWebviewPanel(
            'lrden-guardian-analysis',
            'LRDEnE Guardian Analysis',
            vscode.ViewColumn.One,
            {}
        );

        panel.webview.html = this.getAnalysisDetailsHtml(analysis);
    }

    private getAnalysisDetailsHtml(analysis: GuardianAnalysis): string {
        return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LRDEnE Guardian Analysis</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 20px; }
                .status { padding: 15px; border-radius: 8px; margin-bottom: 20px; }
                .safe { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
                .warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
                .danger { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
                .metric { margin-bottom: 10px; }
                .issues, .recommendations { margin-top: 20px; }
                ul { padding-left: 20px; }
                li { margin-bottom: 5px; }
            </style>
        </head>
        <body>
            <h1>🛡️ LRDEnE Guardian Analysis</h1>
            
            <div class="status ${analysis.is_safe ? 'safe' : 'warning'}">
                <h2>${analysis.is_safe ? '✅ Safe Content' : '⚠️ Requires Review'}</h2>
                <p><strong>Risk Level:</strong> ${analysis.risk_level.toUpperCase()}</p>
                <p><strong>Guardian Score:</strong> ${analysis.guardian_score.toFixed(3)}</p>
                <p><strong>Confidence:</strong> ${(analysis.confidence_score * 100).toFixed(1)}%</p>
            </div>
            
            <div class="summary">
                <h3>Summary</h3>
                <p>${analysis.analysis_summary}</p>
            </div>
            
            ${analysis.detected_issues.length > 0 ? `
            <div class="issues">
                <h3>🚨 Detected Issues</h3>
                <ul>
                    ${analysis.detected_issues.map(issue => `<li>${issue}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
            
            ${analysis.recommendations.length > 0 ? `
            <div class="recommendations">
                <h3>💡 Recommendations</h3>
                <ul>
                    ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
            
            <div class="metadata">
                <h3>Analysis Metadata</h3>
                <p><strong>Timestamp:</strong> ${new Date(analysis.timestamp).toLocaleString()}</p>
                <p><strong>Analysis ID:</strong> ${Math.random().toString(36).substr(2, 9)}</p>
            </div>
        </body>
        </html>
        `;
    }

    private updateStatusBar(message?: string, type?: string) {
        if (message) {
            this.statusBarItem.text = message;
            this.statusBarItem.color = type === 'safe' ? '#11998e' : type === 'warning' ? '#fc4a1a' : undefined;
        } else {
            this.statusBarItem.text = '🛡️ LRDEnE Guardian';
            this.statusBarItem.color = undefined;
        }
        this.statusBarItem.tooltip = 'LRDEnE Guardian - AI Safety Protection';
        this.statusBarItem.show();
    }
}

class AnalysisProvider implements vscode.TreeDataProvider<AnalysisItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<AnalysisItem | undefined | null | void> = new vscode.EventEmitter<AnalysisItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<AnalysisItem | undefined | null | void> = this._onDidChangeTreeData.event;
    
    private analyses: GuardianAnalysis[] = [];

    addAnalysis(analysis: GuardianAnalysis) {
        this.analyses.unshift(analysis);
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element?: AnalysisItem): vscode.TreeItem {
        if (!element) {
            return new AnalysisItem('Recent Analyses', vscode.TreeItemCollapsibleState.Expanded);
        }
        
        return element;
    }

    getChildren(element?: AnalysisItem): Thenable<AnalysisItem[]> {
        if (!element) {
            return Promise.resolve([new AnalysisItem('Recent Analyses', vscode.TreeItemCollapsibleState.Expanded)]);
        }
        
        if (element.label === 'Recent Analyses') {
            return Promise.resolve(this.analyses.slice(0, 10).map((analysis, index) => 
                new AnalysisItem(
                    `${new Date(analysis.timestamp).toLocaleTimeString()} - ${analysis.risk_level.toUpperCase()}`,
                    vscode.TreeItemCollapsibleState.None,
                    analysis
                )
            ));
        }
        
        return Promise.resolve([]);
    }
}

class AnalysisItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly analysis?: GuardianAnalysis
    ) {
        super(label, collapsibleState);
        
        this.tooltip = this.analysis ? 
            `Guardian Score: ${this.analysis.guardian_score.toFixed(3)}\nRisk: ${this.analysis.risk_level}\nSafe: ${this.analysis.is_safe}` : 
            undefined;
        
        this.contextValue = this.analysis ? 'analysis' : 'folder';
        
        if (this.analysis) {
            this.iconPath = this.analysis.is_safe ? 
                new vscode.ThemeIcon('check') : 
                new vscode.ThemeIcon('warning');
        }
    }
}

export function activate(context: vscode.ExtensionContext) {
    const extension = new LRDEnEGuardianExtension();
    
    // Register tree provider
    vscode.window.registerTreeDataProvider('lrden-guardian.analysis', extension.analysisProvider);
    
    // Register commands
    const commands = extension.registerCommands();
    context.subscriptions.push(...commands);
    
    // Register providers
    context.subscriptions.push(
        vscode.workspace.registerTextEditorContentProvider(new GuardianContentProvider())
    );
    
    console.log('LRDEnE Guardian extension activated');
}

export function deactivate() {}

class GuardianContentProvider implements vscode.TextDocumentContentProvider {
    provideTextDocumentContent(uri: vscode.Uri): vscode.ProviderResult<string> {
        return null;
    }
}
