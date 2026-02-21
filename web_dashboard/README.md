# 🛡️ LRDEnE Guardian Web Dashboard

A modern, user-friendly web interface for the LRDEnE Guardian AI safety system.

## 🚀 Features

### For Non-Developers
- **Drag & Drop Interface** - Easy file upload and content analysis
- **Visual Results** - Color-coded safety scores with intuitive displays
- **One-Click Analysis** - Simple content validation without coding
- **Interactive Demo** - See the system in action with real examples

### For Senior Developers
- **API Sandbox** - Test endpoints directly in the browser
- **Interactive Documentation** - Live API testing and examples
- **Real-time Monitoring** - Performance metrics and analytics
- **Integration Ready** - Clean REST API for easy integration

## 📦 Installation

### Prerequisites
- Python 3.8+
- LRDEnE Guardian package installed

### Setup
```bash
# Clone the repository
git clone https://github.com/LOrdEnRYQuE/lrden-guardian.git
cd lrden-guardian/web_dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python app.py
```

## 🌐 Usage

### Starting the Dashboard
```bash
python app.py
```

The dashboard will be available at:
- **Main Interface**: http://localhost:5000
- **API Documentation**: http://localhost:5000/docs
- **Interactive Demo**: http://localhost:5000/demo

### Features Overview

#### 1. Main Dashboard (`/`)
- **Content Analysis**: Enter text or upload files for analysis
- **Real-time Results**: See safety scores, risk levels, and recommendations
- **Visual Metrics**: Guardian Score and Confidence indicators
- **Quick Stats**: System performance overview

#### 2. API Documentation (`/docs`)
- **Interactive API Tester**: Test endpoints directly in browser
- **Code Examples**: Python, JavaScript, and cURL examples
- **Live API Info**: Real-time system information
- **Comprehensive Docs**: Complete API reference

#### 3. Interactive Demo (`/demo`)
- **Pre-loaded Scenarios**: Safe content, hallucination, security risks
- **Visual Analytics**: Animated charts and metrics
- **Performance Tracking**: Demo statistics and averages
- **Educational**: Learn how the system works

## 🔧 API Endpoints

### Analyze Text Content
```http
POST /analyze
Content-Type: application/json

{
  "content": "Text to analyze...",
  "context": {
    "domain": "technical",
    "content_type": "documentation"
  }
}
```

### Analyze File Upload
```http
POST /analyze-file
Content-Type: multipart/form-data

file: [File content]
```

### Get API Information
```http
GET /api-info
```

## 🎨 Customization

### Styling
The dashboard uses Tailwind CSS for styling. Customize the appearance by:
- Editing `templates/base.html` for global styles
- Modifying color schemes in the `<style>` sections
- Adding new components to individual templates

### Configuration
Default settings can be adjusted in `app.py`:
- `MAX_CONTENT_LENGTH`: Maximum file upload size
- `SECRET_KEY`: Flask secret key
- `UPLOAD_FOLDER`: Temporary file storage location

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e ../

EXPOSE 5000
CMD ["python", "app.py"]
```

### Production Deployment
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 Features in Detail

### Non-Developer Friendly
- **No Code Required**: Simple web interface
- **Drag & Drop**: Easy file uploads
- **Visual Feedback**: Clear safety indicators
- **One-Click Reports**: Instant analysis results

### Developer Focused
- **RESTful API**: Clean, documented endpoints
- **Interactive Testing**: Built-in API sandbox
- **Code Examples**: Ready-to-use snippets
- **Performance Metrics**: Real-time monitoring

### Enterprise Ready
- **Secure**: Proper authentication and validation
- **Scalable**: Handles multiple concurrent users
- **Monitoring**: Built-in performance tracking
- **Extensible**: Easy to customize and extend

## 🛡️ Security Features

- **Input Validation**: All content is properly sanitized
- **File Upload Security**: Type and size restrictions
- **Rate Limiting**: Prevents abuse of the API
- **Error Handling**: Graceful error responses

## 📈 Analytics & Monitoring

The dashboard provides:
- **Real-time Metrics**: Processing time, accuracy rates
- **Usage Statistics**: Number of analyses, risk detection
- **Performance Tracking**: Guardian score averages
- **System Health**: Availability and response times

## 🤝 Contributing

We welcome contributions! Please see our main repository for guidelines.

## 📄 License

Copyright (c) 2026 LRDEnE. All rights reserved.

## 🏢 About LRDEnE

LRDEnE is a leading provider of AI safety and content validation solutions. Our mission is to ensure the integrity and safety of AI-powered applications across industries.

---

*🛡️ LRDEnE Guardian - Your AI Safety Partner*
