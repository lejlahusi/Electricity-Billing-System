# ⚡ Electricity Billing System

A FastAPI-powered web application for managing electricity consumption data, generating dynamic billing reports, and exporting PDF invoices.


---

## 🚀 Features

- Upload CSV files with consumption and pricing data
- Automatically parse and store customer records
- View customer list with filters by billing month
- Generate clean PDF bills
- Responsive frontend with loading spinner and download triggers

---

## 📦 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: HTML, JavaScript (DataTables)
- **PDF Generation**: WeasyPrint
- **Styling**: Custom CSS 

---

## 📁 File Structure

app/ 
├── main.py # FastAPI entry point 
├── models.py # SQLAlchemy models 
├── schemas.py # Pydantic schemas 
├── crud.py # DB operations 
├── templates/ # HTML templates 
├── static/ # JS, CSS 
reports/ # Generated PDF bills 
electricna_energija.db # SQLite database

---

## 📤 Upload Format

CSV files must follow this naming convention:
**naloga-lokacija-costumer_id.csv**


And contain the following columns:

- `Časovna Značka (CEST/CET)`
- `Poraba [kWh]`
- `Dinamične Cene [EUR/kWh]`

---

## 🧪 Local Development

### Clone the repository
```bash
git clone https://github.com/lejlahusi/Electricity-Billing-System.git
cd Electricity-Billing-System
```

### Create and activate virtual environment
```bash
python -m venv myvenv
source myvenv/bin/activate  # On Windows use: myvenv\Scripts\activate
```

## Run without docker
```bash
pip install -r requirements.txt # install dependencies
uvicorn app.main:app --reload #run the app 
```

## Run with docker
```bash
# Build and run with Docker
docker-compose up --build

# Access the app
http://127.0.0.1:8000/
```

## Future updates
- Create mailing sistem with STMP.
-  Currently search on table works and will work, but buttons like `Send emails to all`, `Month selection`(to filter billing months) need to be added.
- Also PDF invoice look needs to get updated with logo and more information like costumer address and diagrams with most electrical usage.

## 📜 License
This project is licensed under the [MIT License](LICENCE). Feel free to use, modify, and distribute with attribution.
