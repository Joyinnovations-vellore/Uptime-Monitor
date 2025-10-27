# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. "Error occurred while scraping parts"

This is the most common issue. Here are the likely causes and solutions:

#### **Cause 1: Backend API Not Running**
**Solution:**
```bash
# Start the backend server
python start_backend.py
# OR
python main.py
```

**Check if API is running:**
```bash
# Test the health endpoint
curl http://localhost:8000/health
```

#### **Cause 2: Missing Dependencies**
**Solution:**
```bash
# Install all required packages
pip install -r requirements.txt

# If you get permission errors:
pip install --user -r requirements.txt
```

#### **Cause 3: CORS Issues**
**Solution:**
- Make sure your frontend is running on `http://localhost:3000`
- Check that the backend CORS settings include your frontend URL
- Restart both frontend and backend

#### **Cause 4: Network/Connection Issues**
**Solution:**
```bash
# Test API connectivity
python test_api.py
```

### 2. "No data retrieved" / Empty results

#### **Cause 1: Invalid Part Information**
**Solution:**
- Use valid manufacturer names (Festo, SMC, Siemens, etc.)
- Use real part IDs that exist on manufacturer websites
- Try the sample data first

#### **Cause 2: Website Blocking**
**Solution:**
- Some websites block automated requests
- Try different part numbers
- Check if the manufacturer website is accessible

#### **Cause 3: Selector Issues**
**Solution:**
- The CSS selectors might not match the website structure
- Try updating the selectors in the scraping service

### 3. Frontend Not Loading

#### **Cause 1: Node.js Dependencies**
**Solution:**
```bash
# Install frontend dependencies
npm install

# If you get errors:
npm install --legacy-peer-deps
```

#### **Cause 2: Port Conflicts**
**Solution:**
```bash
# Check if ports are in use
netstat -an | grep :3000
netstat -an | grep :8000

# Kill processes if needed
# Windows:
taskkill /f /im node.exe
# Linux/Mac:
pkill -f node
```

### 4. AI Enrichment Not Working

#### **Cause 1: Missing OpenAI API Key**
**Solution:**
1. Create a `.env` file in the root directory
2. Add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```
3. Restart the backend server

#### **Cause 2: API Key Invalid**
**Solution:**
- Verify your OpenAI API key is correct
- Check if you have sufficient credits
- Try a different API key

### 5. Export Not Working

#### **Cause 1: No Data to Export**
**Solution:**
- Make sure scraping completed successfully
- Check that results are not empty
- Try with sample data first

#### **Cause 2: File Permission Issues**
**Solution:**
```bash
# Check directory permissions
ls -la data/
ls -la templates/

# Fix permissions if needed
chmod 755 data/
chmod 755 templates/
```

## 🧪 Testing Your Setup

### Step 1: Test Backend
```bash
# Run the test script
python test_api.py
```

### Step 2: Test Frontend
```bash
# Start frontend
npm start

# Should open at http://localhost:3000
```

### Step 3: Test Full Workflow
1. Open the application in your browser
2. Add a part with sample data:
   - Manufacturer: Festo
   - Part ID: B10099368
   - Description: Pneumatic cylinder
3. Click "Start Scraping"
4. Check results

## 🔍 Debug Mode

### Enable Debug Logging
Add this to your `.env` file:
```
LOG_LEVEL=DEBUG
```

### Check Logs
```bash
# Backend logs
python main.py

# Frontend logs (in browser console)
F12 -> Console tab
```

## 📞 Getting Help

### Check These First:
1. ✅ Backend is running on port 8000
2. ✅ Frontend is running on port 3000
3. ✅ All dependencies are installed
4. ✅ .env file exists with API key
5. ✅ No firewall blocking connections

### Common Error Messages:

| Error | Cause | Solution |
|-------|-------|----------|
| "Connection refused" | Backend not running | Start backend server |
| "CORS error" | Frontend/backend mismatch | Check URLs and restart |
| "Module not found" | Missing dependencies | Run `pip install -r requirements.txt` |
| "API key invalid" | Wrong OpenAI key | Check .env file |
| "No results" | Scraping failed | Try sample data first |

### Still Having Issues?

1. **Check the browser console** (F12) for JavaScript errors
2. **Check the backend logs** for Python errors
3. **Try the test script** to isolate the problem
4. **Start with sample data** to verify the workflow

## 🚀 Quick Fix Commands

```bash
# Complete reset
rm -rf node_modules
npm install
pip install -r requirements.txt
python start_backend.py
```

```bash
# Check everything is working
python test_api.py
curl http://localhost:8000/health
```

```bash
# Clear all data and start fresh
rm -rf data/*
rm -rf templates/*
python start_backend.py
```
