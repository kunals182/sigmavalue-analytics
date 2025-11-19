🏙️ Sigmavalue Analytics AI
A professional Full Stack Real Estate Intelligence Chatbot built for the Sigmavalue Developer Assessment. This application transforms raw real estate datasets into actionable insights using natural language processing, dynamic data visualization, and fuzzy logic comparison engines.


🚀 Key Features

🧠 Intelligent Analysis
Smart Data Ingestion: Upload any Excel (.xlsx) or CSV dataset via the chat interface.
Fuzzy Location Matching: Finds locations even with partial or slightly misspelled names (e.g., "Ambegaon" finds "Ambegaon Budruk").
Context-Aware Logic: Automatically detects "Price" vs "Demand" queries based on keywords like sales, sold, rates, growth.

📊 Advanced Visualization
Interactive Charts: Dynamic Line Charts powered by Recharts with custom tooltips and legends.
Multi-Location Comparison: Compare trends for multiple areas simultaneously (e.g., "Compare Wakad and Aundh").
Time-Travel Filtering: Handles specific time constraints like "Show prices for the last 3 years".

💎 Premium UI/UX
Glassmorphism Design: Modern, clean interface with gradients and shadows.
User-Centric flow: Typing indicators, auto-scrolling, and empty state suggestions.
Instant Export: One-click Download CSV for filtered data tables.


🛠️ Tech Stack
Component
Technology Used
Frontend
React.js (Vite), Axios, Recharts, Bootstrap 5
Backend
Django REST Framework, Python 3.10+
Data Science
Pandas, NumPy, OpenPyXL
Utils
Regex Parsing, JSON Serialization, Fuzzy Search

⚙️ Installation & Setup Guide
Follow these steps to run the project locally.
📦 1. Backend Setup (Django)
Prerequisites: Python installed.
Navigate to the backend folder:
cd backend


Create and activate a virtual environment:
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


Install dependencies and run the server:
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
✅ Server will start at: http://127.0.0.1:8000/

💻 2. Frontend Setup (React)
Prerequisites: Node.js installed.
Open a new terminal and navigate to the frontend folder:
cd frontend


Install the required packages:
npm install


Start the development server:
npm run dev
✅ App will open at: http://localhost:5173/
🧪 How to Use (Demo Scenarios)
Once the app is running, try these scenarios to test the robust logic:
Step 1: Upload Data
Click the 📎 Paperclip Icon (bottom left) and upload the Sample_data.xlsx provided in the assignment. Wait for the confirmation message.
Step 2: Run Queries
Type these exact queries to see the AI in action:
Single Location Trend:"Analyze Wakad"
Expected Output: A price trend line chart for Wakad and a summary of growth.
Comparison Analysis:"Compare Ambegaon Budruk and Aundh demand trends"
Expected Output: A multi-line chart comparing "Units Sold" for both locations.
Complex Time Filter:"Show price growth for Akurdi over the last 3 years"
Expected Output: Data filtered to show only the most recent 3 years.
Step 3: Export Results
After any analysis, click the "Download CSV" button located above the data table to save the results.

<img width="812" height="461" alt="image" src="https://github.com/user-attachments/assets/483002ae-e2ae-4309-afb0-a1d69254be21" />


🎥 Demo Video
## 🎥 Demo Video
**[Click Here to Watch the Full Demo Video](https://drive.google.com/file/d/1Fh1Hc3yo4rLRBns2bcW6bYe-y3Guxuec/view?usp=drive_link)**

