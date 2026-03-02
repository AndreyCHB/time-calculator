from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="Калькулятор Времени")
templates = Jinja2Templates(directory="templates")
history = []


class ItemCalcRequest(BaseModel):
    item_name: str
    price: float
    hourly_wage: float


class WasteCalcRequest(BaseModel):
    hours_per_day: float
    hourly_wage: float


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/history")
async def get_history():
    return {"history": history[-5:]}


@app.post("/api/calc_item")
async def calc_item(data: ItemCalcRequest):
    hours_needed = round(data.price / data.hourly_wage, 1)
    work_days_needed = round(hours_needed / 8, 1)
    work_months_needed = round(work_days_needed / 22, 1)

    if work_months_needed >= 1:
        time_str = f"{work_months_needed} рабочих месяцев"
    elif work_days_needed >= 1:
        time_str = f"{work_days_needed} рабочих дней"
    else:
        time_str = f"{hours_needed} часов"

    result_text = (f"Чтобы купить «{data.item_name}», вам нужно отдать {time_str} своей жизни "
                   f"({hours_needed} рабочих часов чистыми).")

    history.append({"time": datetime.now().strftime("%H:%M:%S"), "result": result_text})
    return {"status": "success", "result": result_text}


@app.post("/api/calc_waste")
async def calc_waste(data: WasteCalcRequest):
    hours_per_year = data.hours_per_day * 365
    lost_money = round(hours_per_year * data.hourly_wage, 2)
    books_could_read = int(hours_per_year / 6)

    result_text = (f"За год вы сжигаете {hours_per_year} часов.\n"
                   f"💸 Упущенный доход: {lost_money:,.0f} руб.\n"
                   f"📚 Вместо этого вы могли бы прочитать {books_could_read} книг!")

    history.append({"time": datetime.now().strftime("%H:%M:%S"), "result": result_text})
    return {"status": "success", "result": result_text}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8090, reload=True)