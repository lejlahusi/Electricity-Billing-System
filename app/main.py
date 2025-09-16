# Copyright (c) 2025 Lejla Husić
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import csv
import logging
import os
from datetime import datetime
from io import StringIO

from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from weasyprint import HTML

from . import crud, schemas
from .db import get_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

logging.basicConfig(
    filename='app.log',           # File where logs are saved
    level=logging.INFO,           # Minimum severity level to log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Format for timestamps
)
logger = logging.getLogger(__name__)
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, FastAPI!"})


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Extract costumer_id from filename
    filename_parts = file.filename.split("-")
    if len(filename_parts) < 3:
        return {"error": "Filename format must be 'naloga-lokacija-costumer_id.csv'"}

    costumer_id_from_filename = filename_parts[-1].replace(".csv", "").strip()

    contents = await file.read()
    decoded = contents.decode("utf-8").lstrip('\ufeff')
    reader = csv.DictReader(StringIO(decoded),delimiter=';')  # tab-separated
    total_price=0.0
    total_consumption=0.0
    records=[]
    for row in reader:
        timestamp_str = row.get("Časovna Značka (CEST/CET)")
        consumption_str = row.get("Poraba [kWh]")
        price_str = row.get("Dinamične Cene [EUR/kWh]")
        logger.info(timestamp_str)
        if not (timestamp_str and consumption_str and price_str):
            continue  # skip incomplete rows

        # Create consumption record
        total_price+=float(consumption_str.replace(",", "."))*float(price_str.replace(",", "."))
        total_consumption+=float(consumption_str.replace(",", "."))
        records.append(schemas.ConsumptionCreate(
            timestamp=timestamp_str,
            consumption=float(consumption_str.replace(",", ".")),
            price=float(price_str.replace(",", ".")),
            costumer_id=costumer_id_from_filename
        ))
    try:
        crud.create_consumptions(db, records)  # bulk insert
    except Exception:
        logger.exception("Bulk insert failed")
    timestamp_str = timestamp_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(timestamp_str)
    billing_month = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    logging.info(billing_month)
    costumer_data=crud.get_costumer(db, costumer_id=costumer_id_from_filename)
    logging.info(costumer_data.name)
    try:
        if not crud.get_bill(db,costumer_id_from_filename,billing_month):
            billing_data=schemas.BillCreate(
                costumer_id=costumer_data.costumer_id,
                name=costumer_data.name,
                email=costumer_data.email,
                billing_month=billing_month,
                billing_value=total_price,
                billing_consumption=total_consumption
            )
            crud.create_bill(db,billing_data)
            logging.info(billing_data)
    except Exception:
            logger.exception("Exception")
    return {"message": f"CSV data inserted for costumer_id '{costumer_id_from_filename}'"}


@app.post("/costumer-information")
async def submit_form(
    name: str = Form(...,alias="name"),
    email: str = Form(...,alias="email"),
    customer_id: str = Form(...,alias="costumer_id"),
    db: Session = Depends(get_db)
):
    logger.info(name)
    if not crud.get_costumer(db, costumer_id=customer_id):
        costumer_data = schemas.CostumerCreate(
            costumer_id=customer_id,
            name=name,  # optional
            email=email  # required by schema
        )
        crud.create_costumer(db, costumer_data)
    else:
        return {"message": "Costumer already exists."}
    

    return RedirectResponse(url="/", status_code=303)

def get_bills_for_customer_and_month(customer_id: str, month: datetime) -> list[dict]:
    # Replace with actual DB query
    return [
        {"description": "Electricity", "amount": 80.00},
        {"description": "Water", "amount": 40.50}
    ]

@app.get("/get-customers")
async def costumer(request: Request,db: Session = Depends(get_db)):
    logger.info("clicked")
    customers=crud.get_costumers(db)
    logging.info(customers)
    return customers

@app.get("/get-bills")
async def bills(request: Request,db: Session = Depends(get_db)):
    bills=crud.get_bills(db)
    return bills

@app.post("/render-file")
async def render_file(request: Request):
    data = await request.json()

    name = data["name"]
    email = data["email"]
    customer_id = data["costumer_id"]
    billing_month = data["billing_month"][:7]  # "YYYY-MM"
    dt = datetime.strptime(billing_month, "%Y-%m")
    billing_month = dt.strftime("%B, %Y")
    billing_value = float(data["billing_value"])
    billing_consumption = float(data["billing_consumption"])
    today = datetime.today().strftime("%Y-%m-%d")

    #filename = f"bill_report-{customer_id}_{billing_month}.pdf"
    #filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)

    # with open(filepath, "w", encoding="utf-8") as f:
    #     f.write("╔════════════════════════════════════════════════════╗\n")
    #     f.write("║                ELECTRICITY BILL REPORT             ║\n")
    #     f.write("╚════════════════════════════════════════════════════╝\n\n")

    #     f.write(f"Name           : {name}\n")
    #     f.write(f"Email          : {email}\n")
    #     f.write(f"Customer ID    : {customer_id}\n")
    #     f.write(f"Billing Month  : {billing_month}\n")
    #     f.write(f"Generated Date : {today}\n")

    #     f.write("\n" + "─" * 55 + "\n")
    #     f.write(f"{'Billing Total Consumption':<35} {billing_consumption:>10.2f} kW\n")
    #     f.write(f"{'Total Billing Value':<35} €{billing_value:>10.2f}\n")
    #     f.write("─" * 55 + "\n")
    

    html_content = f"""
    <html>
      <head>
        <style>
          @page {{
            size: A4;
            margin: 20mm;
          }}
          body {{
            font-family: Arial, sans-serif;
            background-color: #fff;
            color: #333;
            padding: 0;
            margin: 0;
          }}
          .container {{
            width: 100%;
            box-sizing: border-box;
          }}
          h1 {{
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
          }}
          .info {{
            font-size: 14px;
            margin-bottom: 10px;
          }}
          .section {{
            margin-top: 30px;
            border-top: 1px solid #999;
            padding-top: 15px;
            font-size: 16px;
          }}
          .label {{
            display: inline-block;
            width: 60%;
          }}
          .value {{
            display: inline-block;
            width: 35%;
            text-align: right;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Electricity Bill Report</h1>
          <div class="info"><strong>Name:</strong> {name}</div>
          <div class="info"><strong>Email:</strong> {email}</div>
          <div class="info"><strong>Customer ID:</strong> {customer_id}</div>
          <div class="info"><strong>Billing Month:</strong> {billing_month}</div>
          <div class="info"><strong>Generated Date:</strong> {today}</div>

          <div class="section">
            <div><span class="label">Billing Total Consumption</span><span class="value">{billing_consumption:.2f} kW</span></div>
            <div><span class="label">Total Billing Value</span><span class="value" style="font-size: large;">€{billing_value:.2f}</span></div>
          </div>
        </div>
      </body>
    </html>
    """

    pdf_path = f"reports/bill_report-{customer_id}_{billing_month}.pdf"
    HTML(string=html_content).write_pdf(pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))
