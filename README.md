# توضیحات برنامه Thread-Proccess
پروژه‌ای آموزشی برای نمایش تفاوت بین **Thread** و **Process** در پایتون با استفاده از تکنیک های همزمانی و سناریو های مختلف و تکنولوژی هایی از قبیل  از **FastAPI** و **HTMX**.  
این پروژه به‌صورت کامل **Dockerized** شده است.

---

##  ویژگی‌ها

- اجرای همزمان وظایف با **Threading**
- اجرای موازی وظایف با **Multiprocessing**
- رابط کاربری ساده و سبک با **HTMX**
- پروژه **Dockerized**


---

## ساختار پروژه

```text
Thread-Proccess/
├── main.py
├── Dockerfile
├── .gitignore
├── .dockerignore
├── templates/
│   └── index.html
└── سایر فایل‌های پروژه
```
---
 ## اجرای پروژه با Docker
 ---
1) ساخت ایمیج
- docker build -t thread-proccess .

2) اجرای کانتینر
- docker run -d -p 8000:8000 thread-proccess

3) مشاهده پروژه
- http://localhost:8000

---
 ## نحوه ارسال تغییرات به GitHub
هر بار که تغییری ایجاد شد:
- git status
- git add .
- git commit -m "Description"
- git push

## تکنولوژی‌های استفاده‌شده
- Python 3.10
- FastAPI
- HTMX
- Uvicorn
- Docker
- Threading / Multiprocessing

## توسعه‌دهنده
- میثم ملکی
- شماره دانشجویی: 40411415015


