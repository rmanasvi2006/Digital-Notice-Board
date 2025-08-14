 📢 Digital Notice Board

A web-based **Digital Notice Board** built with **Python (Flask)**, designed to simplify sharing event notices, departmental updates, and important announcements.  
The backend uses **Google Sheets** for real-time data storage and retrieval, eliminating the need for a traditional database.

---

## ✨ Features

- **📄 Post and View Notices**  
  Add new notices that appear instantly for all users.

- **🔍 Sorting Options**  
  Sort notices by **latest**, **oldest**, or **custom criteria** for quick access.

- **🏛 Department-wise Filtering**  
  View notices related to a specific department (e.g., CSE, ECE, MECH) to reduce clutter.

- **💬 Query/Comment Box**  
  Users can click a notice to open its details and submit questions or comments directly.

- **📱 Responsive UI**  
  Works seamlessly on desktops, tablets, and mobile devices.

- **⚡ Real-time Updates**  
  Google Sheets integration ensures that any updates appear without manual refresh.

---

## 🛠 Tech Stack

- **Language:** Python 3.x  
- **Framework:** Flask  
- **Frontend:** HTML, CSS, JavaScript (Bootstrap for styling)  
- **Backend Storage:** Google Sheets (via Google Sheets API)  
- **Libraries Used:**  
  - `Flask` – Web framework  
  - `gspread` – Google Sheets API wrapper  
  - `oauth2client` – Authentication for Google API  
  - `pandas` – Data handling and sorting  

---

## 📂 Project Structure
digital-notice-board/
│
├── static/ # CSS, JS, and image assets
├── templates/ # HTML templates (Flask Jinja2)
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── credentials.json # Google API credentials
└── README.md

markdown
Copy
Edit

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
- Python 3.8+
- Google Cloud account
- Google Sheets document (created and shared with service account email)

### 2️⃣ Enable Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable **Google Sheets API**.
3. Create a service account and download the `credentials.json` file.
4. Share your Google Sheet with the service account email (Editor access).

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
4️⃣ Run the App
bash
Copy
Edit
python app.py
Open http://127.0.0.1:5000 in your browser.

🚀 Usage
Add a Notice: Fill in the form to post a new notice to Google Sheets.

Sort Notices: Choose sorting options from the dropdown.

Filter by Department: Click on a department tag to see relevant notices only.

Ask a Question: Open a notice and use the query box to submit questions or comments.

View in Real Time: All changes are reflected instantly via Google Sheets integration.

🔮 Future Enhancements
User authentication for posting notices.

Email notifications for new notices.

Admin dashboard for managing and deleting notices.

Advanced search by keywords.

📄 License
MIT License © 2025 rmanasvi



