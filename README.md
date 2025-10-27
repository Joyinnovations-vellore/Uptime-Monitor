# Web Scraping & AI Enrichment Application

A comprehensive web scraping and AI-powered data enrichment platform built with FastAPI backend and React frontend.

## 🚀 Features

### Backend (FastAPI)
- **Web Scraping**: BeautifulSoup-powered scraping with custom CSS selectors
- **AI Integration**: GPT/Grok AI assistant for data enrichment
- **Data Processing**: Pandas for data manipulation and Excel export
- **Template System**: Save and reuse scraping configurations
- **Export Options**: Excel (.xlsx) and JSON export formats
- **Async Processing**: High-performance asynchronous operations

### Frontend (React 18+)
- **Modern UI**: Tailwind CSS with dark/light mode toggle
- **Interactive Components**: JSON input, results tables, statistics
- **Animations**: Framer Motion for smooth transitions
- **Copy-to-Clipboard**: Easy data sharing functionality
- **Responsive Design**: Mobile-first approach

### Database & Storage
- **JSON Files**: Template storage and enriched data persistence
- **Excel Export**: Pandas-powered Excel file generation
- **File Management**: Organized data and template directories

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **Libraries**:
  - Pandas (data processing & Excel export)
  - BeautifulSoup (web scraping)
  - Requests (HTTP requests)
  - Pydantic (data validation & JSON parsing)
  - OpenAI (AI integration)
  - aiohttp (async HTTP client)

### Frontend
- **Framework**: React 18+
- **Styling**: Tailwind CSS
- **Icons**: Lucide Icons
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

### Testing
- **API Testing**: Postman collection included
- **Development**: Hot reload for both frontend and backend

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd scraping-final
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key
   ```

5. **Run the backend**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database/Storage Configuration
DATA_DIR=data
TEMPLATES_DIR=templates

# Logging Configuration
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/scrape` | Scrape URLs with selectors |
| POST | `/enrich` | AI-powered data enrichment |
| POST | `/export` | Export data (Excel/JSON) |
| GET | `/templates` | Get all templates |
| POST | `/templates` | Save new template |
| GET | `/templates/{name}` | Get specific template |
| GET | `/statistics` | Get processing statistics |

## 🚀 Usage

### 1. Start the Application

**Backend:**
```bash
python main.py
```

**Frontend:**
```bash
npm start
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 3. Web Scraping Workflow

1. **Configure URLs**: Enter target URLs to scrape
2. **Set Selectors**: Define CSS selectors for data extraction
3. **Save Template**: Optionally save configuration for reuse
4. **Start Scraping**: Execute scraping process
5. **AI Enrichment**: Enhance data with AI insights
6. **Export Data**: Download results in Excel or JSON format

### 4. API Testing with Postman

Import the provided `postman_collection.json` into Postman to test all API endpoints.

## 📊 Features Overview

### Dashboard
- System health monitoring
- Key performance metrics
- Quick action buttons
- Recent activity feed

### Scraping Interface
- Multi-URL scraping
- Custom CSS selector configuration
- Template management
- Real-time preview

### Results Viewer
- Data visualization
- AI enrichment options
- Export functionality
- JSON data inspection

### Statistics
- Performance analytics
- Usage metrics
- Storage information
- Activity charts

## 🎨 UI Features

### Dark/Light Mode
- Automatic system preference detection
- Manual toggle option
- Persistent theme selection

### Animations
- Smooth page transitions
- Loading indicators
- Interactive hover effects
- Progress animations

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interactions

## 🔒 Security Features

- CORS configuration
- Input validation with Pydantic
- Error handling and logging
- Rate limiting (configurable)

## 📈 Performance

### Backend Optimizations
- Async/await operations
- Connection pooling
- Efficient data processing
- Memory management

### Frontend Optimizations
- Code splitting
- Lazy loading
- Optimized bundle size
- Efficient re-renders

## 🧪 Testing

### API Testing
Use the provided Postman collection to test all endpoints:

1. Import `postman_collection.json` into Postman
2. Set the `base_url` variable to `http://localhost:8000`
3. Run the collection tests

### Manual Testing
1. Start both backend and frontend
2. Navigate through all UI components
3. Test scraping with sample URLs
4. Verify data export functionality

## 🚀 Deployment

### Backend Deployment
```bash
# Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Using gunicorn (production)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve with nginx or similar
```

## 📝 API Documentation

### Scraping Request
```json
{
  "urls": ["https://example.com"],
  "selectors": {
    "title": "h1",
    "content": ".content"
  },
  "template_name": "optional_template"
}
```

### Enrichment Request
```json
{
  "data": [{"url": "https://example.com", "title": "Example"}],
  "enrichment_prompt": "Extract key insights",
  "ai_model": "gpt-3.5-turbo"
}
```

### Export Request
```json
{
  "data": [{"url": "https://example.com", "title": "Example"}],
  "format": "excel",
  "filename": "export_file"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the Postman collection
3. Check the console for error messages
4. Verify environment configuration

## 🔄 Updates

### Version 1.0.0
- Initial release
- Complete scraping and AI enrichment functionality
- Modern React frontend with Tailwind CSS
- Comprehensive API with FastAPI
- Postman collection for testing
