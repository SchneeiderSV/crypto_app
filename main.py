from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import requests
from fastapi.staticfiles import StaticFiles
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATABASE = 'transactions.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                          (id INTEGER PRIMARY KEY, cryptocurrency TEXT, amount REAL, brl_value REAL, date TEXT)''')
        conn.commit()

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def get_crypto(request: Request):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cryptocurrency, amount, brl_value, date FROM transactions ORDER BY id DESC LIMIT 10")
            transactions = cursor.fetchall()
        return templates.TemplateResponse("index.html", {"request": request, "transactions": transactions})
    except Exception as e:
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)

@app.post("/calculate", response_class=HTMLResponse)
async def calculate_crypto(request: Request, cryptocurrency: str = Form(...), brl_value: float = Form(...)):
    response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cryptocurrency}&vs_currencies=brl")
    data = response.json()
    crypto_value = data[cryptocurrency]['brl']
    amount = brl_value / crypto_value

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (cryptocurrency, amount, brl_value, date) VALUES (?, ?, ?, ?)",
                   (cryptocurrency, amount, brl_value, date))
    conn.commit()
    cursor.execute("SELECT cryptocurrency, amount, brl_value FROM transactions ORDER BY id DESC LIMIT 10")
    transactions = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse("result.html", {"request": request, "cryptocurrency": cryptocurrency, "amount": amount, "brl_value": brl_value, "transactions": transactions})


@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request, crypto: str = Query(...)):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT date, amount, brl_value FROM transactions WHERE cryptocurrency = ? ORDER BY date ASC", (crypto,))
            history = cursor.fetchall()
        return JSONResponse([{"date": t[0], "crypto_value": t[2]/t[1]} for t in history])
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
