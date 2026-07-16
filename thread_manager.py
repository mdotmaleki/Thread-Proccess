from asyncio import threads
import threading
import time
import os
from threading import Thread
from random import randint, shuffle, randrange
import random
from multiprocessing import Process, Manager
import multiprocessing
from process_manager import ProcessManager
from threading import Barrier, Thread
from time import ctime, sleep
from random import randrange

class MyThreadClass(Thread):
        def __init__(self, name, duration, logs):
            Thread.__init__(self)
            self.name = name
            self.duration = duration
            self.logs = logs

        def run(self):
            self.logs.append(f"---> {self.name} running, belonging to process ID {os.getpid()}")
            time.sleep(self.duration)
            self.logs.append(f"---> {self.name} over")


class FactoryRobot(Thread):
    def __init__(self, robot_name, task, duration, logs):
        Thread.__init__(self)
        self.robot_name = robot_name
        self.task = task
        self.duration = duration
        self.logs = logs

    def run(self):
        self.logs.append(f"[{self.robot_name}] شروع کار: {self.task} — PID={os.getpid()}")
        time.sleep(self.duration)
        self.logs.append(f"[{self.robot_name}] پایان کار: {self.task} (مدت: {self.duration}s)")


class FileWorker(Thread):
    def __init__(self, name, size_mb, logs):
        Thread.__init__(self)
        self.name = name
        self.size_mb = size_mb   # حجم فایل
        self.logs = logs

    def run(self):
        self.logs.append(f"[{self.name}] شروع دانلود فایل ({self.size_mb}MB) — PID={os.getpid()}")

        # مرحله ۱: دانلود
        time.sleep(randint(1, 3))
        self.logs.append(f"[{self.name}] دانلود کامل شد")

        # مرحله ۲: پردازش
        time.sleep(randint(1, 2))
        self.logs.append(f"[{self.name}] پردازش فایل انجام شد")

        # مرحله ۳: ذخیره‌سازی
        time.sleep(randint(1, 2))
        self.logs.append(f"[{self.name}] فایل ذخیره شد")


class LockClass(Thread):
    threadLock = threading.Lock()
    def __init__(self, name, duration, logs):
        Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.logs = logs

    def run(self):
        self.threadLock.acquire()
        self.logs.append(f"{self.name} running (PID={os.getpid()})")
        time.sleep(self.duration)
        self.logs.append(f"{self.name} finished")
        self.threadLock.release()







class ThreadManager:

    
                
   
    def my_func(self, thread_number):
            self.logs.append(f"my_func called by thread N°{thread_number}")
            time.sleep(randint(1, 3))
    
    def worker_func(self, thread_number, task):
            time.sleep(randint(1, 3))

            if task == "sum":
                result = sum(range(1, 50))
            elif task == "multiply":
                result = 1
                for i in range(1, 10):
                    result *= i
            elif task == "random":
                result = randint(1, 100)
            elif task == "string":
                result = f"Thread-{thread_number}"
            elif task == "factorial":
                result = 1
                for i in range(1, 7):
                    result *= i
            elif task == "reverse":
                result = str(thread_number)[::-1]
            elif task == "power":
                result = thread_number ** 3
            elif task == "mod":
                result = thread_number % 3
            elif task == "concat":
                result = f"T{thread_number}_OK"
            elif task == "square":
                result = thread_number * thread_number
            else:
                result = "unknown"

            finish_time = time.strftime("%H:%M:%S", time.localtime())

            self.logs.append(
                f"Thread {thread_number} → task={task} → result={result} → finished at {finish_time}"
            )

    
    # -------------------------
    # Thread + Define + Scenario 1
    # -------------------------        
    def thread_define_1(self):
        self.logs = []


        threads = []

        start = time.time()


        for i in range(10):
            t = Thread(target=self.my_func, args=(i,))
            threads.append(t)
            t.start()
            t.join()  

        total = time.time() - start
        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return self.logs
    # -------------------------

    # -------------------------
    # Thread + Define + Scenario 2
    # -------------------------
    def thread_define_2(self):
        self.logs = []

        threads = []

        start = time.time()

        for i in range(10):
            t = Thread(target=self.my_func, args=(i,))
            threads.append(t)
            t.start() 

    
        for t in threads:
            t.join()

        total = time.time() - start
        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return self.logs
    # -------------------------

    # -------------------------
    # Thread + Define + Scenario 3
    # -------------------------
    def thread_define_3(self):
        self.logs = []

        tasks = [
            "sum",
            "multiply",
            "random",
            "string",
            "factorial",
            "reverse",
            "power",
            "mod",
            "concat",
            "square"
        ]

        threads = []

        start = time.time()

    
        for i in range(10):
            t = Thread(target=self.worker_func, args=(i, tasks[i]))
            threads.append(t)
            t.start()

        
        for t in threads:
            t.join()

        total = time.time() - start
        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return self.logs
    # -------------------------

#--------------------------------------------------End of Define Section-------------------------------------------


#--------------------------------------------------Current Section--------------------------------------------------
    
    def function_A(self, logs):
        logs.append(f"{threading.current_thread().name} --> starting\n")
        time.sleep(2)
        logs.append(f"{threading.current_thread().name} --> exiting\n")

    def function_B(self, logs):
        logs.append(f"{threading.current_thread().name} --> starting\n")
        time.sleep(2)
        logs.append(f"{threading.current_thread().name} --> exiting\n")

    def function_C(self, logs):
        logs.append(f"{threading.current_thread().name} --> starting\n")
        time.sleep(2)
        logs.append(f"{threading.current_thread().name} --> exiting\n")

    def calc_sum(self, logs):
            name = threading.current_thread().name
            logs.append(f"{name} --> starting")
            total = sum(range(1, 101))
            time.sleep(1)
            logs.append(f"{name} --> result = {total}")
            logs.append(f"{name} --> exiting")

    def print_messages(self, logs):
        name = threading.current_thread().name
        logs.append(f"{name} --> starting")
        for i in range(5):
            logs.append(f"{name} --> message {i+1}")
            time.sleep(0.5)
        logs.append(f"{name} --> exiting")

    def random_number(self, logs):
        name = threading.current_thread().name
        logs.append(f"{name} --> starting")
        time.sleep(2)
        num = random.randint(100, 999)
        logs.append(f"{name} --> generated = {num}")
        logs.append(f"{name} --> exiting")

    def download_file(self, logs):
            name = threading.current_thread().name
            logs.append(f"{name} --> starting")
            for i in range(3):
                time.sleep(1)
                logs.append(f"{name} --> downloading chunk {i+1}/3")
            logs.append(f"{name} --> exiting")

    def process_data(self, logs):
        name = threading.current_thread().name
        logs.append(f"{name} --> starting")
        time.sleep(1)
        logs.append(f"{name} --> cleaning data")
        time.sleep(1)
        logs.append(f"{name} --> transforming data")
        time.sleep(1)
        logs.append(f"{name} --> exiting")

    def save_results(self, logs):
        name = threading.current_thread().name
        logs.append(f"{name} --> starting")
        time.sleep(2)
        logs.append(f"{name} --> writing to disk")
        time.sleep(1)
        logs.append(f"{name} --> exiting")

    # -------------------------
    # Thread + Current + Scenario 1
    # -------------------------
    def thread_current_1(self):
        logs = []

        t1 = Thread(name='function_A', target=self.function_A, args=(logs,))
        t2 = Thread(name='function_B', target=self.function_B, args=(logs,))
        t3 = Thread(name='function_C', target=self.function_C, args=(logs,))

        start = time.time()

    
        t1.start()
        t2.start()
        t3.start()

    
        t1.join()
        t2.join()
        t3.join()

        total = time.time() - start
        logs.append("End")
        logs.append(f"{total:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + Current + Scenario 2
    # -------------------------
    def thread_current_2(self):
        logs = []

        
        t1 = Thread(name="calc_sum", target=self.calc_sum, args=(logs,))
        t2 = Thread(name="print_messages", target=self.print_messages, args=(logs,))
        t3 = Thread(name="random_number", target=self.random_number, args=(logs,))

        start = time.time()

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        total = time.time() - start
        logs.append("End")
        logs.append(f"{total:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + Current + Scenario 3
    # -------------------------
    def thread_current_3(self):
        logs = []

        

        t1 = Thread(name="download_file", target=self.download_file, args=(logs,))
        t2 = Thread(name="process_data", target=self.process_data, args=(logs,))
        t3 = Thread(name="save_results", target=self.save_results, args=(logs,))

        start = time.time()

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        total = time.time() - start
        logs.append("End")
        logs.append(f"{total:.2f} seconds")

        return logs
    # -------------------------

#--------------------------------------------------End of Current Section--------------------------------------------------

#--------------------------------------------------Subclass Section--------------------------------------------------

    # -------------------------
    # Thread + Subclass + Scenario 1
    # -------------------------
    def thread_subclass_1(self):
        logs = []

        

        start_time = time.time()

        threads = [
            MyThreadClass(f"Thread#{i} ", randint(1,10), logs)
            for i in range(1, 10)
        ]


        for t in threads:
            t.start()

        for t in threads:
            t.join()



        logs.append("End")
        logs.append(f"{time.time() - start_time:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + Subclass + Scenario 2
    # -------------------------
    def thread_subclass_2(self):
        logs = []

        

        start_time = time.time()

        # ساخت 9 نخ با حجم فایل تصادفی
        threads = [
            FileWorker(f"Worker#{i}", randint(5, 50), logs)
            for i in range(1, 10)
        ]

        # اجرای نخ‌ها
        for t in threads:
            t.start()

        # منتظر پایان همه نخ‌ها
        for t in threads:
            t.join()

        logs.append("End")
        logs.append(f"{time.time() - start_time:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + Subclass + Scenario 3
    # -------------------------
    def thread_subclass_3(self):
        logs = []

        tasks = [
            "جوشکاری قطعات",
            "رنگ‌کاری بدنه",
            "بسته‌بندی محصول",
            "کنترل کیفیت",
            "مونتاژ اولیه",
            "مونتاژ نهایی",
            "لیزرکاری",
            "چاپ سریال",
            "تست عملکرد"
        ]

        start_time = time.time()

    
        threads = [
            FactoryRobot(
                robot_name=f"Robot#{i}",
                task=tasks[i % len(tasks)],
                duration=randint(1, 4),
                logs=logs
            )
            for i in range(1, 10)
        ]


        for t in threads:
            t.start()


        for t in threads:
            t.join()

        logs.append("End")
        logs.append(f"{time.time() - start_time:.2f} seconds")

        return logs
    # -------------------------

#--------------------------------------------------End of Subclass Section--------------------------------------------------

#--------------------------------------------------Lock Section--------------------------------------------------

    # -------------------------
    # Thread + Lock + Scenario 1
    # -------------------------
    def thread_lock_1(self):
        
        logs = []

        threads = [
            LockClass(f"Thread#{i}", randint(1, 3), logs=logs)
            for i in range(1, 10)
        ]

        start = time.time()

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        total = time.time() - start
        logs.append("End")
        logs.append(f"{total:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + Lock + Scenario 2
    # -------------------------
    def thread_lock_2(self):
        page_lock = threading.Lock()
        logs = []

        webpage = {"content": ""}

        class User(Thread):
            def __init__(self, name):
                Thread.__init__(self)
                self.name = name
                self.start_delay = randint(0, 3)

            def run(self):
                
                time.sleep(self.start_delay)

                
                page_lock.acquire()

                logs.append(f"{self.name} شروع به نوشتن کرد")

                
                time.sleep(randint(1, 3))

                text = f"متن نوشته شده توسط {self.name}\n"

                old_content = webpage["content"]
                new_content = old_content + text
                webpage["content"] = new_content

                logs.append(f"{self.name} متن را به صفحه اضافه کرد")
                logs.append(f"{self.name} نوشتن را تمام کرد")

                
                page_lock.release()

        users = [User(f"کاربر {i+1}") for i in range(5)]

        for u in users:
            u.start()

        for u in users:
            u.join()

        logs.append("محتوای نهایی صفحه:")
        logs.append(webpage["content"])

        return logs
    
    # -------------------------

    # -------------------------
    # Thread + Lock + Scenario 3
    # -------------------------
    def thread_lock_3(self):
        seat_lock = threading.Lock()
        logs = []

        seats = list(range(1, 11))
        shuffle(seats)

        logs.append(f"لیست اولیه صندلی‌ها: {seats}")

        class Customer(Thread):
            def __init__(self, cid):
                Thread.__init__(self)
                self.cid = cid
                self.arrival_delay = randint(0, 2)

            def run(self):
                
                time.sleep(self.arrival_delay)

                
                seat_lock.acquire()

                
                available = seats.copy()
                logs.append(f"مشتری {self.cid} → لیست را دید: {available}")

                
                chosen_seat = available[0]
                logs.append(f"مشتری {self.cid} → صندلی {chosen_seat} را انتخاب کرد")

                
                time.sleep(randint(1, 3))

                
                if chosen_seat in seats:
                    seats.remove(chosen_seat)
                    logs.append(f"مشتری {self.cid} → صندلی {chosen_seat} را رزرو کرد")
                else:
                    logs.append(f"مشتری {self.cid} → صندلی {chosen_seat} قبلاً رزرو شده بود")

                logs.append(f"مشتری {self.cid} → کارش تمام شد")

                
                seat_lock.release()

        customers = [Customer(i+1) for i in range(10)]

        for c in customers:
            c.start()

        for c in customers:
            c.join()

        logs.append(f"صندلی‌های باقی‌مانده: {seats}")
        return logs
    # -------------------------

    # -------------------------
    # Thread + RLock + Scenario 1
    # -------------------------
    def thread_rlock_1(self):
        logs = []

        class Box:
            def __init__(self):
                self.lock = threading.RLock()
                self.total_items = 0

            def execute(self, value):
                with self.lock:
                    self.total_items += value

            def add(self):
                with self.lock:
                    self.execute(1)

            def remove(self):
                with self.lock:
                    self.execute(-1)

        def adder(box, items):
            logs.append(f"N° {items} items to ADD")
            while items:
                box.add()
                time.sleep(1)
                items -= 1
                logs.append(f"ADDED one item --> {items} item(s) left to ADD")

        def remover(box, items):
            logs.append(f"N° {items} items to REMOVE")
            while items:
                box.remove()
                time.sleep(1)
                items -= 1
                logs.append(f"REMOVED one item --> {items} item(s) left to REMOVE")

        
        box = Box()

        
        t1 = threading.Thread(target=adder, args=(box, random.randint(10, 20)))
        t2 = threading.Thread(target=remover, args=(box, random.randint(1, 10)))

        start_time = time.time()

        
        t1.start()
        t2.start()

        
        t1.join()
        t2.join()

        logs.append("End")
        logs.append(f"Final total_items = {box.total_items}")
        logs.append(f"{time.time() - start_time:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + RLock + Scenario 2
    # -------------------------
    def thread_rlock_2(self):
        logs = []

        class BankAccount:
            def __init__(self, name, balance):
                self.name = name
                self.balance = balance
                self.lock = threading.RLock()

            def update_balance(self):
                with self.lock:
                   
                    time.sleep(0.2)
                    logs.append(f"[{self.name}] موجودی به‌روزرسانی شد → {self.balance}")

            def deposit(self, amount):
                with self.lock:
                    self.balance += amount
                    logs.append(f"[{self.name}] واریز {amount} انجام شد → موجودی جدید: {self.balance}")
                    self.update_balance()

            def withdraw(self, amount):
                with self.lock:
                    if self.balance >= amount:
                        self.balance -= amount
                        logs.append(f"[{self.name}] برداشت {amount} انجام شد → موجودی جدید: {self.balance}")
                        self.update_balance()
                    else:
                        logs.append(f"[{self.name}] برداشت {amount} ناموفق → موجودی کافی نیست")

            def transfer(self, target_account, amount):
                with self.lock:
                    logs.append(f"شروع انتقال {amount} از {self.name} به {target_account.name}")
                    self.withdraw(amount)
                    target_account.deposit(amount)
                    logs.append(f"انتقال {amount} از {self.name} به {target_account.name} انجام شد")

     
        acc1 = BankAccount("حساب A", 1000)
        acc2 = BankAccount("حساب B", 500)

        logs.append(f"موجودی اولیه حساب A: {acc1.balance}")
        logs.append(f"موجودی اولیه حساب B: {acc2.balance}")

        
        def task1():
            acc1.transfer(acc2, 300)

        def task2():
            acc2.deposit(200)
            time.sleep(1)
            acc2.withdraw(100)

        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)

        start = time.time()

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        logs.append("End")
        logs.append(f"موجودی نهایی حساب A: {acc1.balance}")
        logs.append(f"موجودی نهایی حساب B: {acc2.balance}")
        logs.append(f"{time.time() - start:.2f} seconds")

        return logs
    # -------------------------


    # -------------------------
    # Thread + RLock + Scenario 3
    # -------------------------
    def thread_rlock_3(self):
        logs = []

        class ShoppingCart:
            def __init__(self, owner):
                self.owner = owner
                self.items = []
                self.total_price = 0
                self.lock = threading.RLock()

            def update_total(self):
                with self.lock:
                    time.sleep(0.2)
                    self.total_price = sum(price for _, price in self.items)
                    logs.append(f"[{self.owner}] مجموع قیمت به‌روزرسانی شد → {self.total_price}")

            def add_item(self, name, price):
                with self.lock:
                    self.items.append((name, price))
                    logs.append(f"[{self.owner}] افزودن کالا: {name} ({price})")
                    self.update_total()

            def remove_item(self, name):
                with self.lock:
                    for item in self.items:
                        if item[0] == name:
                            self.items.remove(item)
                            logs.append(f"[{self.owner}] حذف کالا: {name}")
                            self.update_total()
                            return
                    logs.append(f"[{self.owner}] کالا {name} یافت نشد")

            def checkout(self):
                with self.lock:
                    logs.append(f"[{self.owner}] شروع تسویه حساب...")
                    time.sleep(0.5)
                    self.update_total()
                    logs.append(f"[{self.owner}] تسویه حساب انجام شد → مبلغ نهایی: {self.total_price}")

        
        cart1 = ShoppingCart("سبد A")
        cart2 = ShoppingCart("سبد B")

        
        logs.append("سبدها قبل از شروع عملیات:")
        logs.append(f"سبد A → مجموع: {cart1.total_price}")
        logs.append(f"سبد B → مجموع: {cart2.total_price}")

        
        def task1():
            cart1.add_item("کتاب", 120)
            cart1.add_item("خودکار", 20)
            cart1.remove_item("کتاب")
            cart1.checkout()

        def task2():
            cart2.add_item("کفش", 300)
            time.sleep(1)
            cart2.add_item("جوراب", 50)
            cart2.checkout()

        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)

        start = time.time()

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        logs.append("End")
        logs.append(f"مجموع نهایی سبد A: {cart1.total_price}")
        logs.append(f"مجموع نهایی سبد B: {cart2.total_price}")
        logs.append(f"{time.time() - start:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + Semaphore + Scenario 3
    # -------------------------
    def thread_semaphore_1(self):
        logs = []

        NUM = 5
        forks = [threading.Semaphore(1) for _ in range(NUM)]
        room = threading.Semaphore(4)

        
        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        def philosopher(i):
            name = f"Philosopher-{i}"

            
            make_log(name, "در حال فکر کردن...")

            room.acquire()

            make_log(name, "درخواست چنگال چپ")
            forks[i].acquire()

            make_log(name, "درخواست چنگال راست")
            forks[(i + 1) % NUM].acquire()

            make_log(name, "در حال غذا خوردن...")
            time.sleep(random.uniform(0.5, 1.5))

            make_log(name, "رهاسازی چنگال‌ها")
            forks[i].release()
            forks[(i + 1) % NUM].release()

            room.release()

            make_log(name, "تمام شد، برگشت به فکر کردن")

        start = time.time()

        threads = []
        for i in range(NUM):
            t = threading.Thread(target=philosopher, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("End")
        logs.append(f"{time.time() - start:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + Semaphore + Scenario 1
    # -------------------------
    def thread_semaphore_2(self):
        logs = []

        NUM_CHAIRS = 3
        waiting = 0

        customers = threading.Semaphore(0)
        barber = threading.Semaphore(0)
        mutex = threading.Semaphore(1)

        
        def make_log(thread_name, message):
            logs.append(f"{thread_name} ---> {message}")

    
        def barber_thread():
            nonlocal waiting
            name = "آرایشگر"

            while True:
                make_log(name, "در حال خوابیدن...")
                customers.acquire()

                mutex.acquire()
                waiting -= 1
                make_log(name, f"یک مشتری را صدا زد (منتظرها: {waiting})")
                mutex.release()

                barber.release()

                make_log(name, "در حال اصلاح مو...")
                time.sleep(random.uniform(1, 2))

        
        def customer_thread(i):
            nonlocal waiting
            name = f"مشتری-{i}"

            make_log(name, "وارد آرایشگاه شد")

            mutex.acquire()
            if waiting < NUM_CHAIRS:
                waiting += 1
                make_log(name, f"روی صندلی نشست (منتظرها: {waiting})")
                customers.release()
                mutex.release()

                barber.acquire()
                make_log(name, "در حال اصلاح مو")
                time.sleep(random.uniform(0.5, 1.5))
                make_log(name, "آرایش تمام شد و رفت")
            else:
                make_log(name, "جا نبود، برگشت")
                mutex.release()

        
        t_barber = threading.Thread(target=barber_thread, daemon=True)
        t_barber.start()

        threads = []
        for i in range(10):
            t = threading.Thread(target=customer_thread, args=(i+1,))
            threads.append(t)
            t.start()
            time.sleep(random.uniform(0.3, 1))

        for t in threads:
            t.join()

        logs.append("End")
        return logs

    # -------------------------

    # -------------------------
    # Thread + Semaphore + Scenario 3
    # -------------------------
    def thread_semaphore_3(self):
        logs = []

        
        db_semaphore = threading.Semaphore(5)

        
        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        
        def access_database(thread_name):
            make_log(thread_name, "درخواست اتصال به دیتابیس")

            db_semaphore.acquire()
            make_log(thread_name, "اتصال برقرار شد")

            
            time.sleep(random.uniform(1, 3))

            make_log(thread_name, "اتصال آزاد شد")
            db_semaphore.release()

        start = time.time()

        threads = []

        
        for i in range(20):
            t_name = f"Thread-{i+1}"
            t = threading.Thread(target=access_database, args=(t_name,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("End")
        logs.append(f"{time.time() - start:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + condition + Scenario 1
    # -------------------------
    def thread_condition_1(self):
        logs = []

        items = []
        condition = threading.Condition()

        # تابع کمکی برای ساخت لاگ
        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        # -------------------------------
        # Consumer
        # -------------------------------
        def consume(thread_name):
            with condition:
                if len(items) == 0:
                    make_log(thread_name, "no items to consume")
                    condition.wait()

                items.pop()
                make_log(thread_name, "consumed 1 item")
                condition.notify()

        def consumer_thread():
            name = "Consumer"
            for _ in range(20):
                time.sleep(2)
                consume(name)

        # -------------------------------
        # Producer
        # -------------------------------
        def produce(thread_name):
            with condition:
                if len(items) == 10:
                    make_log(thread_name, f"items produced {len(items)}. Stopped")
                    condition.wait()

                items.append(1)
                make_log(thread_name, f"total items {len(items)}")
                condition.notify()

        def producer_thread():
            name = "Producer"
            for _ in range(20):
                time.sleep(0.5)
                produce(name)

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        start = time.time()

        t1 = threading.Thread(target=producer_thread)
        t2 = threading.Thread(target=consumer_thread)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        logs.append("End")
        logs.append(f"{time.time() - start:.2f} seconds")

        return logs
    # -------------------------


    # -------------------------
    # Thread + condition + Scenario 2
    # -------------------------
    def thread_condition_2(self):
        logs = []

        queue = []                 # صف کارهای چاپ
        condition = threading.Condition()
        MAX_QUEUE = 5              # ظرفیت صف چاپ

        # تابع کمکی برای ساخت لاگ
        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        # -------------------------------
        # Printer (Consumer)
        # -------------------------------
        def printer_thread():
            name = "Printer"

            while True:
                with condition:
                    while len(queue) == 0:
                        make_log(name, "no print jobs, sleeping...")
                        condition.wait()

                    job = queue.pop(0)
                    make_log(name, f"printing job {job}")
                    condition.notify()

                time.sleep(1.5)  # زمان چاپ

        # -------------------------------
        # Employee (Producer)
        # -------------------------------
        def employee_thread(i):
            name = f"Employee-{i}"

            for j in range(3):  # هر کارمند 3 کار چاپ می‌فرستد
                time.sleep(random.uniform(0.5, 2))

                with condition:
                    while len(queue) == MAX_QUEUE:
                        make_log(name, "queue full, waiting...")
                        condition.wait()

                    job_id = f"{i}-{j}"
                    queue.append(job_id)
                    make_log(name, f"submitted print job {job_id}")
                    condition.notify()

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        start = time.time()

        # نخ چاپگر (daemon)
        t_printer = threading.Thread(target=printer_thread, daemon=True)
        t_printer.start()

        # چند کارمند
        threads = []
        for i in range(5):
            t = threading.Thread(target=employee_thread, args=(i+1,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("End")
        logs.append(f"{time.time() - start:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + condition + Scenario 3
    # -------------------------
    def thread_condition_3(self):
        logs = []

        orders = []                 # صف سفارش‌ها
        condition = threading.Condition()
        MAX_ORDERS = 5              # ظرفیت صف سفارش

        # تابع کمکی برای ساخت لاگ
        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        # -------------------------------
        # Chef (Consumer)
        # -------------------------------
        def chef_thread():
            name = "Chef"

            while True:
                with condition:
                    while len(orders) == 0:
                        make_log(name, "no orders, sleeping...")
                        condition.wait()

                    order = orders.pop(0)
                    make_log(name, f"cooking order {order}")
                    condition.notify()

                time.sleep(1.5)  # زمان پخت غذا

        # -------------------------------
        # Waiter (Producer)
        # -------------------------------
        def waiter_thread(i):
            name = f"Waiter-{i}"

            for j in range(3):  # هر گارسون 3 سفارش می‌گیرد
                time.sleep(random.uniform(0.5, 2))

                with condition:
                    while len(orders) == MAX_ORDERS:
                        make_log(name, "order queue full, waiting...")
                        condition.wait()

                    order_id = f"{i}-{j}"
                    orders.append(order_id)
                    make_log(name, f"submitted order {order_id}")
                    condition.notify()

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        start = time.time()

        # نخ آشپز (daemon)
        t_chef = threading.Thread(target=chef_thread, daemon=True)
        t_chef.start()

        # چند گارسون
        threads = []
        for i in range(4):
            t = threading.Thread(target=waiter_thread, args=(i+1,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("End")
        logs.append(f"{time.time() - start:.2f} seconds")

        return logs
    # -------------------------


    # -------------------------
    # Thread + event + Scenario 1
    # -------------------------
    def thread_event_1(self):
        logs = []

        items = []                 # بافر مشترک
        event = threading.Event()  # رویداد برای هماهنگی نخ‌ها

        # تابع کمکی برای ساخت لاگ
        def make_log(thread_name, message):
            #timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logs.append(f"{thread_name:} ---> {message}")

        # -------------------------------
        # Consumer (مصرف‌کننده)
        # -------------------------------
        def consumer_thread():
            name = "Consumer"

            while True:
                time.sleep(2)
                event.wait()   # منتظر سیگنال Producer

                if len(items) > 0:
                    item = items.pop()
                    make_log(name, f"consumed item {item}")
                else:
                    make_log(name, "no item to consume")

                event.clear()  # سیگنال مصرف شد، پاک می‌کنیم

        # -------------------------------
        # Producer (تولیدکننده)
        # -------------------------------
        def producer_thread():
            name = "Producer"

            for _ in range(5):
                time.sleep(2)
                item = random.randint(0, 100)
                items.append(item)
                make_log(name, f"produced item {item}")

                event.set()  # سیگنال بده به Consumer

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        start = time.time()

        t1 = threading.Thread(name="Producer", target=producer_thread)
        t2 = threading.Thread(name="Consumer", target=consumer_thread, daemon=True)

        t1.start()
        t2.start()

        t1.join()

        total = time.time() - start
        logs.append("End")
        logs.append(f"{total:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + event + Scenario 2
    # -------------------------
    def thread_event_2(self):
        logs = []

        event = threading.Event()

        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        # -------------------------------
        # عملیات‌های بعد از دانلود
        # -------------------------------
        def reader():
            name = "Reader"
            make_log(name, "waiting for file...")
            event.wait()
            make_log(name, "reading file...")
            time.sleep(random.uniform(0.5, 1.5))
            make_log(name, "finished reading")

        def writer():
            name = "Writer"
            make_log(name, "waiting for file...")
            event.wait()
            make_log(name, "writing to file...")
            time.sleep(random.uniform(0.5, 1.5))
            make_log(name, "finished writing")

        def backup():
            name = "Backup"
            make_log(name, "waiting for file...")
            event.wait()
            make_log(name, "backing up file...")
            time.sleep(random.uniform(0.5, 1.5))
            make_log(name, "finished backup")

        def analyzer():
            name = "Analyzer"
            make_log(name, "waiting for file...")
            event.wait()
            make_log(name, "analyzing file...")
            time.sleep(random.uniform(0.5, 1.5))
            make_log(name, "finished analyzing")

        # -------------------------------
        # Downloader Thread
        # -------------------------------
        def downloader():
            name = "Downloader"

            make_log(name, "starting download...")
            time.sleep(random.uniform(1, 3))
            make_log(name, "download completed")

            # سیگنال بده تا عملیات‌های بعدی شروع شوند
            event.set()

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        start = time.time()

        threading.Thread(target=downloader, name="Downloader").start()
        threading.Thread(target=reader, name="Reader", daemon=True).start()
        threading.Thread(target=writer, name="Writer", daemon=True).start()
        threading.Thread(target=backup, name="Backup", daemon=True).start()
        threading.Thread(target=analyzer, name="Analyzer", daemon=True).start()

        # صبر کن تا همه عملیات‌ها انجام شوند
        time.sleep(5)

        total = time.time() - start
        logs.append("End")
        logs.append(f"{total:.2f} seconds")

        return logs
    # -------------------------

    def thread_event_3(self):
        logs = []

        green_event = threading.Event()   # چراغ سبز
        red_event = threading.Event()     # چراغ قرمز

        car_count = 5                     # تعداد ماشین‌ها
        cycles = 3                        # تعداد چرخه‌ها

        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        # -------------------------------
        # رفتار ماشین‌ها
        # -------------------------------
        def car(car_id):
            name = f"Car-{car_id}"

            make_log(name, "waiting for green light...")

            for cycle in range(1, cycles + 1):

                green_event.wait()   # منتظر چراغ سبز

                make_log(name, f"moving (cycle {cycle})")
                time.sleep(random.uniform(0.5, 1.5))

                red_event.wait()     # منتظر چراغ قرمز
                make_log(name, f"stopped at red light (cycle {cycle})")

            make_log(name, "finished all cycles")

        # -------------------------------
        # چراغ راهنمایی
        # -------------------------------
        def traffic_light():
            name = "TrafficLight"

            for cycle in range(1, cycles + 1):
                make_log(name, f"GREEN light ON (cycle {cycle})")
                red_event.clear()
                green_event.set()

                time.sleep(5)  # مدت زمان چراغ سبز

                make_log(name, f"RED light ON (cycle {cycle})")
                green_event.clear()
                red_event.set()

                time.sleep(3)  # مدت زمان چراغ قرمز

            make_log(name, "all cycles completed")

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        start = time.time()

        # ساخت ماشین‌ها
        for i in range(1, car_count + 1):
            threading.Thread(target=car, args=(i,), name=f"Car-{i}", daemon=True).start()

        # چراغ راهنمایی
        t_light = threading.Thread(target=traffic_light, name="TrafficLight")
        t_light.start()

        t_light.join()

        total = time.time() - start
        logs.append("End")
        logs.append(f"{total:.2f} seconds")

        return logs
    # -------------------------

    # -------------------------
    # Thread + barrier + Scenario 1
    # -------------------------


    def thread_barrier_1(self):
        logs = []

        from random import randrange
        from threading import Barrier, Thread
        from time import ctime, sleep

        num_runners = 3
        finish_line = Barrier(num_runners)
        runners = ['Huey', 'Dewey', 'Louie']

        def runner():
            name = runners.pop()
            sleep(randrange(2, 5))
            logs.append(f"{name} reached the barrier at: {ctime()}")
            finish_line.wait()

        logs.append("START RACE!!!!")

        threads = []
        for i in range(num_runners):
            threads.append(Thread(target=runner))
            threads[-1].start()

        for thread in threads:
            thread.join()

        logs.append("Race over!")

        return logs
    # -------------------------

    # -------------------------
    # Thread + barrier + Scenario 2
    # -------------------------
    def thread_barrier_2(self):
        logs = []

        from threading import Barrier, Thread
        from time import sleep, ctime
        import random

        file_count = 3
        barrier_download = Barrier(file_count)
        barrier_process = Barrier(file_count)

        files = ["file1", "file2", "file3"]

        def make_log(thread_name, message):
            logs.append(f"{thread_name} --> {message}")

        # -------------------------------
        # رفتار هر فایل
        # -------------------------------
        def worker(file_name):

            # مرحله ۱: دانلود
            sleep(random.uniform(1, 3))
            make_log(file_name, f"downloaded at {ctime()}")
            barrier_download.wait()

            # مرحله ۲: پردازش
            sleep(random.uniform(1, 3))
            make_log(file_name, f"processed at {ctime()}")
            barrier_process.wait()

            # مرحله ۳: ذخیره
            sleep(random.uniform(1, 3))
            make_log(file_name, f"saved at {ctime()}")

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        threads = []
        for f in files:
            t = Thread(target=worker, args=(f,), name=f)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("All files downloaded, processed, and saved.")
        return logs
    # -------------------------

    # -------------------------
    # Thread + barrier + Scenario 3
    # -------------------------
    def thread_barrier_3(self):
        logs = []

        from threading import Barrier, Thread
        from time import sleep, ctime
        import random

        product_count = 3

        # سه مرحله، هرکدام یک Barrier
        barrier_build = Barrier(product_count)
        barrier_paint = Barrier(product_count)

        products = ["Product-1", "Product-2", "Product-3"]

        def make_log(name, msg):
            logs.append(f"{name} --> {msg}")

        # -------------------------------
        # رفتار هر محصول
        # -------------------------------
        def worker(product):

            # مرحله ۱: ساخت
            sleep(random.uniform(1, 3))
            make_log(product, f"built at {ctime()}")
            barrier_build.wait()

            # مرحله ۲: رنگ
            sleep(random.uniform(1, 3))
            make_log(product, f"painted at {ctime()}")
            barrier_paint.wait()

            # مرحله ۳: بسته‌بندی
            sleep(random.uniform(1, 3))
            make_log(product, f"packaged at {ctime()}")

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        threads = []
        for p in products:
            t = Thread(target=worker, args=(p,), name=p)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("All products built, painted, and packaged.")
        return logs
    # -------------------------

    # -------------------------
    # Thread + queue + Scenario 1
    # -------------------------
    def thread_queue_1(self):
        logs = []

        from threading import Thread
        from queue import Queue
        import time
        import random

        queue = Queue()

        # -------------------------------
        # Producer
        # -------------------------------
        def producer():
            for i in range(5):
                item = random.randint(0, 256)
                queue.put(item)
                logs.append(f"Producer notify: item Nº{item} appended to queue by Producer")
                time.sleep(1)

        # -------------------------------
        # Consumer
        # -------------------------------
        def consumer(name):
            while True:
                item = queue.get()
                logs.append(f"Consumer notify: {item} popped from queue by {name}")
                queue.task_done()

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        t1 = Thread(target=producer, name="Producer")
        t2 = Thread(target=consumer, args=("Consumer-1",), name="Consumer-1")
        t3 = Thread(target=consumer, args=("Consumer-2",), name="Consumer-2")
        t4 = Thread(target=consumer, args=("Consumer-3",), name="Consumer-3")

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()

        # صبر می‌کنیم تا همهٔ آیتم‌ها پردازش شوند
        queue.join()

        logs.append("Queue processing finished.")

        return logs
    # -------------------------

    # -------------------------
    # Thread + queue + Scenario 2
    # -------------------------
    def thread_queue_2(self):
        logs = []

        from threading import Thread
        from queue import Queue
        import time
        import random

        # صف سفارش‌های آماده
        order_queue = Queue()

        # -------------------------------
        # Producer: آشپزخانه
        # -------------------------------
        def kitchen():
            for i in range(10):  # ده سفارش آماده می‌شود
                order_id = random.randint(1000, 9999)
                order_queue.put(order_id)
                logs.append(f"Kitchen --> Order {order_id} is ready and added to queue")
                time.sleep(random.uniform(0.5, 1.5))

        # -------------------------------
        # Consumer: پیک‌ها
        # -------------------------------
        def delivery_boy(name):
            while True:
                order_id = order_queue.get()
                logs.append(f"{name} --> picked order {order_id} from queue")
                time.sleep(random.uniform(1, 2))  # زمان تحویل
                logs.append(f"{name} --> delivered order {order_id}")
                order_queue.task_done()

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        t_kitchen = Thread(target=kitchen, name="Kitchen")

        delivery_threads = []
        for i in range(1, 4):  # سه پیک
            t = Thread(target=delivery_boy, args=(f"DeliveryBoy-{i}",), name=f"DeliveryBoy-{i}")
            delivery_threads.append(t)

        t_kitchen.start()
        for t in delivery_threads:
            t.start()

        # صبر می‌کنیم تا همه سفارش‌ها تحویل شوند
        t_kitchen.join()
        order_queue.join()

        logs.append("All orders have been delivered.")
        return logs
    # -------------------------

    # -------------------------
    # Thread + queue + Scenario 3
    # -------------------------
    def thread_queue_3(self):
        logs = []

        from threading import Thread
        from queue import Queue
        import time
        import random

        # صف سفارش‌های ثبت‌شده
        order_queue = Queue()

        # -------------------------------
        # Producer: سیستم ثبت سفارش
        # -------------------------------
        def order_system():
            for i in range(12):  # دوازده سفارش تولید می‌کنیم
                order_id = random.randint(10000, 99999)
                order_queue.put(order_id)
                logs.append(f"OrderSystem --> New order {order_id} added to queue")
                time.sleep(random.uniform(0.3, 1.0))

        # -------------------------------
        # Consumer: کارمندهای پردازش سفارش
        # -------------------------------
        def order_processor(name):
            while True:
                order_id = order_queue.get()
                logs.append(f"{name} --> picked order {order_id} from queue")

                # زمان پردازش سفارش
                time.sleep(random.uniform(1.0, 2.0))

                logs.append(f"{name} --> processed order {order_id}")
                order_queue.task_done()

        # -------------------------------
        # اجرای نخ‌ها
        # -------------------------------
        t_producer = Thread(target=order_system, name="OrderSystem")

        processors = []
        for i in range(1, 4):  # سه کارمند
            t = Thread(target=order_processor, args=(f"Processor-{i}",), name=f"Processor-{i}")
            processors.append(t)

        t_producer.start()
        for t in processors:
            t.start()

        # صبر می‌کنیم تا همه سفارش‌ها پردازش شوند
        t_producer.join()
        order_queue.join()

        logs.append("All orders have been processed.")
        return logs
    # -------------------------