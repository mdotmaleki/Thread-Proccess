from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import threading
import time
import os
from threading import Thread
from random import randint

# توضیحات سناریوها
from scenarioRunner import run_scenario
from scenario_descriptions import scenario_descriptions

app = FastAPI()

# اجازه دسترسی از سمت UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# مدل ورودی برای /run
class RunRequest(BaseModel):
    method: str
    tool: str
    scenario: str


@app.get("/", response_class=HTMLResponse)
def home():
    html = Path("templates/index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/get-tools")
def get_tools(method: str):
    if method == "thread":
        return {
            "tools": [
                "define", "current", "subclass", "lock",
                "rlock", "semaphore", "condition","event", "barrier", "queue"
            ]
        }

    if method == "process":
        return {
            "tools": [
                "spawning", "naming", "background", "killing", 
                "subclass", "queue","pipe","barrier", "pool"
            ]
        }

    return {"tools": []}


@app.post("/run")
def run(req: RunRequest):

    method = req.method
    tool = req.tool
    scenario = req.scenario 

    if method in scenario_descriptions \
       and tool in scenario_descriptions[method] \
       and scenario in scenario_descriptions[method][tool]:

        description = scenario_descriptions[method][tool][scenario]
    else:
        return {
            "status": "error",
            "message": f"برای {method} با ابزار {tool} سناریوی {scenario} تعریف نشده است.",
            "description": ""
        }

    logs = run_scenario(method, tool, scenario)

    if logs is None:
        return {
            "status": "error",
            "message": f"برای {method} با ابزار {tool} سناریوی {scenario} تعریف نشده است.",
            "description": ""
        }

    return {
        "status": "ok",
        "logs": logs,
        "description": description
    }


@app.get("/get-scenarios")
def get_scenarios(method: str, tool: str):

    scenario_map = {
        "thread": {
            "define": [
                {"id": "define_1", "title": "تعریف ساده ترتیبی"},
                {"id": "define_2", "title": "تعریف ساده موازی"},
                {"id": "define_3", "title": "تعریف نخ با وظایف مختلف"},
            ],
            "current": [
                {"id": "current_1", "title": "نمایش نام نخ"},
                {"id": "current_2", "title": "نخ های با وظایف مختلف"},
                {"id": "current_3", "title": "شبیه سازی دانلود، پردازش و ذخیره سازی"},
            ],
            "subclass": [
                {"id": "subclass_1", "title": "نخ با استفاده از subclass: مثال کتاب"},
                {"id": "subclass_2", "title": "شبیه سازی دانلود، پردازش و ذخیره سازی"},
                {"id": "subclass_3", "title": "شبیه سازی ربات های کارخانه"},
            ],
            "lock": [
                {"id": "lock_1", "title": "کنترل همزمانی"},
                {"id": "lock_2", "title": "نویسندگان وب"},
                {"id": "lock_3", "title": "رزرو صندلی سینما"},
            ],
            "rlock": [
                {"id": "rlock_1", "title": "مثال کتاب"},
                {"id": "rlock_2", "title": "عملیات بانکی"},
                {"id": "rlock_3", "title": "سبد خرید"},
            ],
            "semaphore": [
                {"id": "semaphore_1", "title": "غذا خوردن فیلسوف‌ها"},
                {"id": "semaphore_2", "title": "آرایشگر خواب آلود"},
                {"id": "semaphore_3", "title": "پایگاه داده"},
                
            ],
            "condition": [
                {"id": "condition_1", "title": "تولید کننده و مصرف کننده"},
                {"id": "condition_2", "title": "صف چاپ"},
                {"id": "condition_3", "title": "سفارش رستوران"},
            ],
            "event": [
                {"id": "event_1", "title": "تولید کننده و مصرف کننده"},
                {"id": "event_2", "title": "پردازش فایل"},
                {"id": "event_3", "title": "چراغ راهنمایی"},
            ],
            "barrier": [
                {"id": "barrier_1", "title": "دونده ها"},
                {"id": "barrier_2", "title": "دانلود و پردازش فایل ها"},
                {"id": "barrier_3", "title": "تولید محصول"},
            ],
            "queue": [
                {"id": "queue_1", "title": "تولید کننده و مصرف کننده"},
                {"id": "queue_2", "title": "سفارش رستوران"},
                {"id": "queue_3", "title": "فروشگاه آنلاین"},
            ],
        },

        "process": {
            "spawning": [
                {"id": "spawn_1", "title": "اجرای ترتیبی"},
                {"id": "spawn_2", "title": "اجرای موازی"},
                {"id": "spawn_3", "title": "فرآیند با وظایف مختلف"},
            ],
            "naming": [
                {"id": "naming_1", "title": "نمایش نام فرآیند ها"},
                {"id": "naming_2", "title": "فرآیندهای با وظایف مختلف"},
                {"id": "naming_3", "title": "کدگذاری، کدگشایی و هش کردن دیتا"},
            ],
            "background": [
                {"id": "background_1", "title": "چاپ اعداد"},
                {"id": "background_2", "title": "اتو سیو"},
                {"id": "background_3", "title": "ارسال و دریافت پیام"},
            ],
             "killing": [
                {"id": "killing_1", "title": "خاتمه فرایند"},
                {"id": "killing_2", "title": "خاتمه فرایندهای طولانی"},
                {"id": "killing_3", "title": "خاتمه فرایند زامبی"},
            ],
            "subclass": [
                {"id": "subclass_1", "title": "چاپ اشیا از کلاس"},
                {"id": "subclass_2", "title": "محاسبه مربع عدد"},
                {"id": "subclass_3", "title": "پردازش پیام ها"},
            ],
            "queue": [
                {"id": "queue_1", "title": "تولید کننده مصرف کننده"},
                {"id": "queue_2", "title": "توزیع وظایف"},
                {"id": "queue_3", "title": "فرستنده و گیرنده"},
            ],
            "pipe": [
                {"id": "pipe_1", "title": "مربع اعداد"},
                {"id": "pipe_2", "title": "معکوس کردن رشته"},
                {"id": "pipe_3", "title": "محاسبه فاکتوریل"},
            ],
            "barrier": [
                {"id": "barrier_1", "title": "همزمانی فرایندها"},
                {"id": "barrier_2", "title": "پردازش تصویر"},
                {"id": "barrier_3", "title": "محاسبه معدل"},
            ],
            "pool": [
                {"id": "pool_1", "title": "اجرای موازی روی مجموعه"},
                {"id": "pool_2", "title": "هش پسورد"},
                {"id": "pool_3", "title": "شمارش کلمات"},
            ],
        }
    }

    # اگر تعریف شده باشد
    if method in scenario_map and tool in scenario_map[method]:
        return {"scenarios": scenario_map[method][tool]}

    # اگر نبود → سناریوی پیش‌فرض
    return {
        "scenarios": [
            {"id": "default_1", "title": "سناریوی پیش‌فرض ۱"},
            {"id": "default_2", "title": "سناریوی پیش‌فرض ۲"},
            {"id": "default_3", "title": "سناریوی پیش‌فرض ۳"},
        ]
    }


    # -------------------------
    # اگر سناریو تعریف نشده باشد
    # -------------------------
    return {
        "status": "error",
        "message": f"برای {method} با ابزار {tool} سناریوی {scenario} تعریف نشده است.",
        "description": ""
    }