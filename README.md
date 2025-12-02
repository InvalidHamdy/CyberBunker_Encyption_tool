<h1 align="center">🛡️ CyberBunker – Encryption Tool</h1>
<p align="center">A multi-algorithm encryption desktop app built with Python & Tkinter.</p>
<p align="center"><b>Secure. Fast. Educational.</b></p>

---

## 🔐 Overview
CyberBunker is a desktop encryption tool showcasing a collection of classical and modern cryptographic algorithms inside a clean, interactive GUI.  
Built with Python, Tkinter, and CustomTkinter, the app includes user authentication, password recovery, file encryption/decryption, and RSA key generation.

---

## 🚀 Features

### 🎨 GUI
- Modern interface using Tkinter + CustomTkinter  
- Dashboard layout for selecting algorithms  
- Includes UI assets: `background3.png`, `Frame 1.png`, `logo.png`

### 🔑 Algorithms Included (in `algorithms/`)
- Caesar Cipher  
- Affine Cipher  
- Vigenère Cipher  
- Playfair Cipher  
- Rail Fence Cipher  
- Substitution Cipher  
- ROT13  
- RSA (key generation + encryption)

### 👤 User System (in `services/`)
- Login & authentication  
- Forgot Password + OTP verification  
- SQLite / SQLiteCloud support  
- Environment-based DB configuration

### 📁 Encryption Workflow
- Encrypt/decrypt text or files  
- File upload, overwrite, and safe output handling  

---

## 🗂️ Project Structure
CyberBunker/
│
├── app.py
├── LogIn.py
├── AlgorithmDashBoard.py
├── EncryptionPage.py
│
├── algorithms/
├── services/
├── database/
│ └── DATABASE_CYBERSECURTY.sql
│
├── assets/
│ ├── background3.png
│ ├── Frame 1.png
│ └── logo.png
│
└── test.py

yaml
Copy code

---

## 🧩 Requirements
- Python 3.8+

Install dependencies:
```bash
pip install -r requirements.txt
requirements.txt should include:

pillow

customtkinter

python-dotenv

sqlitecloud

⚙️ Configuration
Create a .env file:

ini
Copy code
CONNECTION_STRING=<your_sqlitecloud_connection_string_or_local_db_path>
🗄️ Database
A starter SQL schema is included at:

pgsql
Copy code
database/DATABASE_CYBERSECURTY.sql
Review and update column names or data before seeding.

▶️ Running the App
bash
Copy code
python app.py
🧪 Tests
bash
Copy code
python test.py
🧠 Notes
Ensure all image assets exist in the working directory.

DB connection must be configured before login or OTP flows.

Encryption algorithms are modular and easy to extend.

🤝 Contributing
Fork

Create a feature branch

Add any new cipher with tests

Submit a PR

📜 License
No license specified — consider adding one (MIT recommended).

<p align="center">🔐 Built by a security-focused team. Stay encrypted.</p> ```
