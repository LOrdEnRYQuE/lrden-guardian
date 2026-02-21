#!/usr/bin/env python3
"""
LRDEnE Guardian - Web Dashboard
================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Modern web interface for AI safety and hallucination detection.
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lrden_guardian import create_lrden_guardian

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lrden-guardian-web-dashboard-2026'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Guardian
guardian = create_lrden_guardian()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_content():
    """Analyze text content"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        context = data.get('context', {})
        
        if not content.strip():
            return jsonify({'error': 'Content cannot be empty'}), 400
        
        # Analyze content
        result = guardian.analyze_content(content, context)
        
        # Format response
        response = {
            'is_safe': result.is_safe,
            'risk_level': result.risk_level.value,
            'confidence_score': result.confidence_score,
            'guardian_score': result.guardian_score,
            'analysis_summary': result.analysis_summary,
            'recommendations': result.recommendations,
            'detected_issues': result.detected_issues,
            'uncertainty_areas': result.uncertainty_areas,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-file', methods=['POST'])
def analyze_file():
    """Analyze uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read file content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze content
            result = guardian.analyze_content(content)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Format response
            response = {
                'filename': filename,
                'is_safe': result.is_safe,
                'risk_level': result.risk_level.value,
                'confidence_score': result.confidence_score,
                'guardian_score': result.guardian_score,
                'analysis_summary': result.analysis_summary,
                'recommendations': result.recommendations,
                'detected_issues': result.detected_issues,
                'uncertainty_areas': result.uncertainty_areas,
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api-info')
def api_info():
    """API information for developers"""
    return jsonify({
        'name': 'LRDEnE Guardian API',
        'version': '1.0.0',
        'endpoints': {
            'analyze': '/analyze - POST - Analyze text content',
            'analyze-file': '/analyze-file - POST - Analyze uploaded file',
            'api-info': '/api-info - GET - API information'
        },
        'guardian_info': guardian.get_guardian_info()
    })

@app.route('/demo')
def demo():
    """Demo page with examples"""
    return render_template('demo.html')

@app.route('/docs')
def docs():
    """API documentation page"""
    return render_template('docs.html')

if __name__ == '__main__':
    print("🛡️ Starting LRDEnE Guardian Web Dashboard...")
    print("🌐 Dashboard will be available at: http://localhost:5001")
    print("📚 API docs at: http://localhost:5001/docs")
    print("🎯 Demo at: http://localhost:5001/demo")
    app.run(debug=True, host='0.0.0.0', port=5001)
