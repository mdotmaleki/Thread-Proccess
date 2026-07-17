**دانشجو: میثم ملکی**

**شماره دانشجویی: 40411415015**

**درس: پردازش موازی**

**استاد: دکتر رشنو**

# توضیحات برنامه Thread-Process
پروژه‌ای آموزشی برای نمایش تفاوت بین **Thread** و **Process** در پایتون با استفاده از تکنیک های همزمانی و سناریو های مختلف و تکنولوژی هایی از قبیل  از **FastAPI** و **HTMX**.  
این پروژه به‌صورت کامل **Dockerized** شده است.

---

##  ویژگی‌ها

- اجرای همزمان وظایف با **Threading**
- اجرای موازی وظایف با **Multiprocessing**
- رابط کاربری ساده و سبک با **HTMX**
- پروژه **Dockerized**

---
## ثبت دامنه در Cloudflare برای مدیریت آن و استفاده از proxy
![کلودفلر](images/cloudflare.png)
---

---
## تنظیم Cloudflare DNS برای دامنه ثبت شده در IRNIC
![ایرنیک](images/irnic.png)
---

---
## تهیه سرور مجازی VPS از شرکت پارس پک
![پارس پک](images/parspack.png)
---

---
## نصب داکر روی سرور
![داکر](images/docker1.png)
---

---
## نصب نیازمندی ها از فایل Requierments.txt
![نیازمندی ها](images/req.png)
---

---
## Image ساخته شده روی سرور
![image](images/image.png)
---

---
## نصب و پیکربندی nginx
![nginx](images/nginx1.png)
![nginx](images/nginx2.png)
---

---
## استفاده از nginx certbot برای فعالسازی https
![https](images/https1.png)
![https](images/https2.png)
---

## فعالسازی CI/CD برای دیپلوی خودکار تغییرات روی سرور
![cicd](images/cicd.png)
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
## ساختار کلی دسترسی به پروژه
![ساختار کلی درخواست](images/req-tree.jpg)
---

---
 ## پروژه نهایی
 ---

## آدرس
https://meysam-maleki.ir

![site](images/site.png)

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


