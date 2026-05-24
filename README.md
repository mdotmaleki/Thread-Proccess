# توضیحات برنامه Thread-Proccess
پروژه‌ای آموزشی برای نمایش تفاوت بین **Thread** و **Process** در پایتون، با استفاده از **FastAPI** و **HTMX**.  
این پروژه به‌صورت کامل **Dockerized** شده و روی هر سیستمی قابل اجراست.

---

##  ویژگی‌ها

- اجرای همزمان وظایف با **Threading**
- اجرای موازی وظایف با **Multiprocessing**
- رابط کاربری ساده و سبک با **HTMX**
- API سریع و مدرن با **FastAPI**
- آماده برای اجرا داخل **Docker**
- ساختار تمیز و قابل توسعه

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
docker build -t thread-proccess .

2) اجرای کانتینر
docker run -d -p 8000:8000 thread-proccess

3) مشاهده پروژه
مرورگر را باز کنید:
http://localhost:8000

---
 ## نحوه ارسال تغییرات به GitHub
هر بار که تغییری ایجاد شد:
git status
git add .
git commit -m "شرح تغییرات"
git push

## تکنولوژی‌های استفاده‌شده
- Python 3.10
- FastAPI
- HTMX
- Uvicorn
- Docker
- Threading / Multiprocessing

## توسعه‌دهنده
میثم ملکی


