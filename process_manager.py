#from multiprocessing import Barrier, Lock
from multiprocessing import Process
from datetime import datetime
import hashlib
import multiprocessing
#from time import time, sleep
import random
from passlib.context import CryptContext
import multiprocessing
import random
import time
from datetime import datetime
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SquareProcess(multiprocessing.Process):

    def __init__(self, logs, number, index):
        super().__init__(name=f"square_process_{index}")
        self.logs = logs
        self.number = number

    def run(self):
        time.sleep(1)
        square = self.number * self.number
        self.logs.append(f"{self.name}: square({self.number}) = {square}")
        return

class MyProcess(multiprocessing.Process):

    def __init__(self, logs, index):
        super().__init__(name=f"my_process_{index}")
        self.logs = logs
        self.index = index

    def run(self):
        self.logs.append(f"called run method by {self.name}")
        return

class MessageProcess(multiprocessing.Process):

    def __init__(self, logs, message, delay, index):
        super().__init__(name=f"message_processor_{index}")
        self.logs = logs
        self.message = message
        self.delay = delay

    def run(self):
        time.sleep(self.delay)
        self.logs.append(f"{self.name}: {self.message} (after {self.delay} secs)")
        return   

class Producer(multiprocessing.Process):

    def __init__(self, logs, queue):
        super().__init__(name="producer_process")
        self.logs = logs
        self.queue = queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.logs.append(f"[Producer] item {item} appended to queue")
            time.sleep(1)
            self.logs.append(f"[Producer] queue size is {self.queue.qsize()}")

class Consumer(multiprocessing.Process):

    def __init__(self, logs, queue):
        super().__init__(name="consumer_process")
        self.logs = logs
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                self.logs.append("[Consumer] queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                self.logs.append(f"[Consumer] item {item} popped from queue")
                time.sleep(1)

class JobMaker(multiprocessing.Process):

    def __init__(self, logs, queue):
        super().__init__(name="job_maker")
        self.logs = logs
        self.queue = queue

    def run(self):
        job_id = 1
        while job_id <= 12:
            if self.queue.full():
                self.logs.append("queue is full, job_maker waiting...")
                time.sleep(1)
                continue

            job = f"job_{job_id}"
            self.queue.put(job)
            self.logs.append(f"{job} produced by job_maker")
            self.logs.append(f"queue size is {self.queue.qsize()}")
            job_id += 1
            time.sleep(0.5)

class Dispatcher(multiprocessing.Process):

    def __init__(self, logs, queue, worker_queues, busy_flags):
        super().__init__(name="dispatcher")
        self.logs = logs
        self.queue = queue
        self.worker_queues = worker_queues
        self.busy_flags = busy_flags
        self.index = 0

    def run(self):
        while True:
            if self.queue.empty():
                self.logs.append("queue is empty, dispatcher waiting...")
                time.sleep(1)
                continue

            
            free_processor = None
            for i in range(3):
                if not self.busy_flags[i]:
                    free_processor = i
                    break

            if free_processor is None:
                self.logs.append("all processors busy, dispatcher waiting...")
                time.sleep(1)
                continue

            job = self.queue.get()
            self.busy_flags[free_processor] = True

            self.worker_queues[free_processor].put(job)
            self.logs.append(f"{job} sent to processor_{free_processor+1}")
            self.logs.append(f"queue size is {self.queue.qsize()}")

            time.sleep(0.3)

class Processor(multiprocessing.Process):

    def __init__(self, logs, queue, busy_flags, index):
        super().__init__(name=f"processor_{index}")
        self.logs = logs
        self.queue = queue
        self.busy_flags = busy_flags
        self.index = index

    def run(self):
        while True:
            if self.queue.empty():
                time.sleep(0.2)
                continue

            job = self.queue.get()
            self.logs.append(f"processor_{self.index} started {job}")

            time.sleep(random.uniform(1, 2))

            self.logs.append(f"processor_{self.index} finished {job}")
            self.busy_flags[self.index - 1] = False  

class Sender(multiprocessing.Process):

    def __init__(self, logs, queue):
        super().__init__(name="sender")
        self.logs = logs
        self.queue = queue

    def run(self):
        data_id = 1
        while data_id <= 30:
            if self.queue.full():
                self.logs.append("queue full, sender waiting...")
                time.sleep(0.1)
                continue

            data = f"data_{data_id}"
            self.queue.put(data)
            self.logs.append(f"{data} sent by sender")
            self.logs.append(f"queue size is {self.queue.qsize()}")

            data_id += 1
            time.sleep(0.1)

class Receiver(multiprocessing.Process):

    def __init__(self, logs, queue):
        super().__init__(name="receiver")
        self.logs = logs
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                self.logs.append("queue empty, receiver waiting...")
                time.sleep(0.2)
                continue

            data = self.queue.get()
            self.logs.append(f"{data} consumed by receiver")
            self.logs.append(f"queue size is {self.queue.qsize()}")

            time.sleep(0.2) 

class ProducerPipe(multiprocessing.Process):

    def __init__(self, logs, pipe):
        super().__init__(name="producer_pipe")

        self.logs = logs
        self.output_pipe, _ = pipe

    def run(self):

        for i in range(10):

            self.output_pipe.send(i)

            self.logs.append(
                f"{self.name} sent {i}"
            )

            time.sleep(0.5)

        self.output_pipe.close()

        self.logs.append(
            f"{self.name} finished"
        )

class SquarePipe(multiprocessing.Process):

    def __init__(self, logs, pipe_in, pipe_out):
        super().__init__(name="square_pipe")

        self.logs = logs

        self.close_pipe, self.input_pipe = pipe_in

        self.output_pipe, _ = pipe_out

    def run(self):

        self.close_pipe.close()

        try:

            while True:

                number = self.input_pipe.recv()

                result = number * number

                self.output_pipe.send(result)

                self.logs.append(
                    f"{self.name} received {number} -> sent {result}"
                )

        except EOFError:

            self.output_pipe.close()

            self.logs.append(
                f"{self.name} finished"
            )

class StringProducer(multiprocessing.Process):

    def __init__(self, logs, pipe):
        super().__init__(name="string_producer")

        self.logs = logs
        self.output_pipe, _ = pipe

    def run(self):

        words = [
            "Python",
            "Process",
            "Multiprocessing",
            "Pipe",
            "Communication"
        ]

        for word in words:

            self.output_pipe.send(word)

            self.logs.append(
                f"{self.name} sent '{word}'"
            )

            time.sleep(0.5)

        self.output_pipe.close()

        self.logs.append(
            f"{self.name} finished"
        )

class ReverseString(multiprocessing.Process):

    def __init__(self, logs, pipe_in, pipe_out):
        super().__init__(name="reverse_string")

        self.logs = logs

        self.close_pipe, self.input_pipe = pipe_in

        self.output_pipe, _ = pipe_out

    def run(self):

        self.close_pipe.close()

        try:

            while True:

                word = self.input_pipe.recv()

                reversed_word = word[::-1]

                self.output_pipe.send(reversed_word)

                self.logs.append(
                    f"{self.name} received '{word}' -> sent '{reversed_word}'"
                )

        except EOFError:

            self.output_pipe.close()

            self.logs.append(
                f"{self.name} finished"
            )

class NumberProducer(multiprocessing.Process):

    def __init__(self, logs, pipe):
        super().__init__(name="number_producer")

        self.logs = logs
        self.output_pipe, _ = pipe

    def run(self):

        numbers = [3, 4, 5, 6, 7]

        for number in numbers:

            self.output_pipe.send(number)

            self.logs.append(
                f"{self.name} sent {number}"
            )

            time.sleep(0.5)

        self.output_pipe.close()

        self.logs.append(
            f"{self.name} finished"
        )

class FactorialProcess(multiprocessing.Process):

    def __init__(self, logs, pipe_in, pipe_out):
        super().__init__(name="factorial_process")

        self.logs = logs

        self.close_pipe, self.input_pipe = pipe_in

        self.output_pipe, _ = pipe_out

    def factorial(self, number):

        result = 1

        for i in range(2, number + 1):
            result *= i

        return result

    def run(self):

        self.close_pipe.close()

        try:

            while True:

                number = self.input_pipe.recv()

                result = self.factorial(number)

                self.output_pipe.send(result)

                self.logs.append(
                    f"{self.name} received {number} -> sent {result}"
                )

        except EOFError:

            self.output_pipe.close()

            self.logs.append(
                f"{self.name} finished"
            )

class WorkerPool:
    @staticmethod
    def function_square(x):
        return x * x

class HashWorker:

    @staticmethod
    def hash_password(password: str):

        # تبدیل پسورد به هش SHA256
        hashed = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        return hashed

class BarrierWorker(multiprocessing.Process):

    def __init__(self, logs, synchronizer, serializer, use_barrier=True):
        super().__init__()

        self.logs = logs
        self.synchronizer = synchronizer
        self.serializer = serializer
        self.use_barrier = use_barrier


    def run(self):

        name = multiprocessing.current_process().name

        if self.use_barrier:

            self.synchronizer.wait()

            now = time.time()

            with self.serializer:

                self.logs.append(
                    f"{name} ----> {datetime.fromtimestamp(now)}"
                )

        else:

            now = time.time()

            self.logs.append(
                f"{name} ----> {datetime.fromtimestamp(now)}"
            )

class BarrierImageWorker:

    @staticmethod
    def image_processing(barrier, lock, logs, image_name):

        name = multiprocessing.current_process().name

        logs.append(f"{name} -> Processing {image_name}")

        time.sleep(random.randint(1, 4))

        logs.append(f"{name} -> Finished {image_name}")

        # منتظر همه Processها
        barrier.wait()

        with lock:
            logs.append(f"{name} -> Saving {image_name}")

class BarrierAverageWorker:

    @staticmethod
    def calculate_scores(barrier, lock, logs, course):

        name = multiprocessing.current_process().name

        logs.append(f"{name} -> Calculating {course}")

        time.sleep(random.randint(2, 5))

        logs.append(f"{name} -> {course} Finished")

        barrier.wait()

        with lock:
            logs.append(f"{name} -> Publishing {course}")



class ProcessManager:

    def __init__(self):
        self.logs = None

    def process_worker(self, process_number, logs):
        logs.append(
            f"Calling Process_worker from process {process_number}"
        )

        for j in range(0, process_number):
            logs.append(
                f"Output from Process_worker is {j}"
            )

    def download_worker(self, logs):

        logs.append("Download Process started")

        for i in range(1, 4):
            time.sleep(1)
            logs.append(
                f"Downloading file part {i}/3"
            )

        logs.append("Download Process finished")

    def analysis_worker(self, logs):

        logs.append("Analysis Process started")

        numbers = [10, 20, 30, 40, 50]

        result = sum(numbers)

        time.sleep(2)

        logs.append(
            f"Analysis result = {result}"
        )

        logs.append("Analysis Process finished")

    def database_worker(self, logs):

        logs.append("Database Process started")


        data = {
            "user": "Meysam",
            "score": 95
        }


        time.sleep(1)


        logs.append(
            f"Saved data: {data}"
        )


        logs.append(
            "Database Process finished"
        )

    def naming_worker(self):
        name = multiprocessing.current_process().name
        self.logs.append(f"Starting process name = {name}")
        time.sleep(3)
        self.logs.append(f"Exiting process name = {name}")

    def adder_worker(self, numbers, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Starting adder worker")

        result = sum(numbers)
        logs.append(f"[{name}] Sum result = {result}")

        logs.append(f"[{name}] Finished adder worker")

    def randomizer_worker(self, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Starting randomizer worker")

        value = random.randint(1, 100)
        logs.append(f"[{name}] Random value = {value}")

        logs.append(f"[{name}] Finished randomizer worker")

    def reverser_worker(self, text, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Starting reverser worker")

        reversed_text = text[::-1]
        logs.append(f"[{name}] Reversed text = {reversed_text}")

        logs.append(f"[{name}] Finished reverser worker")

    def encrypt_worker(self, text, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Starting encryption")

        encrypted = "".join(chr(ord(c) + 3) for c in text)
        logs.append(f"[{name}] Encrypted result = {encrypted}")

        logs.append(f"[{name}] Finished encryption")

    def decrypt_worker(self, encrypted_text, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Starting decryption")

        decrypted = "".join(chr(ord(c) - 3) for c in encrypted_text)
        logs.append(f"[{name}] Decrypted result = {decrypted}")

        logs.append(f"[{name}] Finished decryption")

    def hash_worker(self, text, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Starting hashing")

        hashed = hashlib.sha256(text.encode()).hexdigest()
        logs.append(f"[{name}] SHA256 hash = {hashed}")

        logs.append(f"[{name}] Finished hashing")

    def background_mode_worker(self, logs):
        name = multiprocessing.current_process().name
        logs.append(f"Starting {name}")

        if name == "background_process":
            for i in range(0, 5):
                logs.append(f"[{name}] ---> {i}")
                time.sleep(1)
        else:
            for i in range(5, 10):
                logs.append(f"[{name}] ---> {i}")
                time.sleep(1)

        logs.append(f"Exiting {name}")

    def writer_worker(self, logs, shared_data):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Writer started")

        for i in range(1, 4):
            logs.append(f"[{name}] writer process is writing...")

            write_time = random.randint(3, 5)
            time.sleep(write_time)

            shared_data["last_write"] = f"Write #{i} completed"
            logs.append(f"[{name}] Write #{i} completed in {write_time} seconds")

        logs.append(f"[{name}] Writer finished")

    def background_saver_worker(self, logs, shared_data):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Background saver started")

        while True:
            time.sleep(1)
            logs.append(f"[{name}] changes saved by background process successfully")

    def writer_worker(self, logs, shared_data):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Writer started")

        for i in range(1, 4):
            write_time = random.randint(3, 5)

            logs.append(f"[{name}] writer process is writing... (duration: {write_time} sec)")
            time.sleep(write_time)

            shared_data["last_write"] = f"Write #{i} completed"
            #logs.append(f"[{name}] Write #{i} completed in {write_time} seconds")

        logs.append(f"[{name}] Writer finished")

    def background_saver_worker(self, logs, shared_data):
        name = multiprocessing.current_process().name
        #logs.append(f"[{name}] Background saver started")

        while True:
            time.sleep(1)
            logs.append(f"[{name}] changes saved by background process successfully")

    def sender_worker(self, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Sender started")

        for i in range(1, 6):
            wait_time = random.randint(2, 4)
            time.sleep(wait_time)

            logs.append(f"[{name}] sender: sent a message number {i}")

        logs.append(f"[{name}] Sender finished")

    def listener_worker(self, logs):
        name = multiprocessing.current_process().name
        logs.append(f"[{name}] Listener started")

        while True:
            logs.append(f"[{name}] reciever is listening ...")

            
            time.sleep(1)
            if random.choice([True, False]):
                msg_number = random.randint(1, 20)
                logs.append(f"[{name}] reciever: A message number {msg_number} recieved")

    def foo_worker(self, logs):
        logs.append("Starting function")

        for i in range(0, 10):
            logs.append(f"---> {i}")
            time.sleep(1)

        logs.append("Finished function")

    def firstWorker(self, logs, index):
        name = multiprocessing.current_process().name
        duration = random.randint(1, 10)
        logs.append(f"{name} started, will take {duration} secs")
        time.sleep(duration)
        logs.append(f"{name} finished normally in {duration} secs")

    def secondWorker(self, logs, index):
        name = multiprocessing.current_process().name
        logs.append(f"{name} is calculating")
        time.sleep(2)
        logs.append(f"{name} finished calculation")



    def spawn_scenario_1(self):

        manager = multiprocessing.Manager()

        self.logs = manager.list()

        start = time.time()


        for i in range(6):

            p = multiprocessing.Process(
                target=self.process_worker,
                args=(i, self.logs)
            )
            p.start()
            p.join()

            


        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")


        return list(self.logs)

    def spawn_scenario_2(self):


        manager = multiprocessing.Manager()

        self.logs = manager.list()

        start = time.time()

        processes = []

        for i in range(6):

            p = multiprocessing.Process(
                target=self.process_worker,
                args=(i, self.logs)
            )

            processes.append(p)
            p.start()


        for p in processes:
            p.join()


        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")


        return list(self.logs)
    
    def spawn_scenario_3(self):

        manager = multiprocessing.Manager()

        logs = manager.list()


        start = time.time()


        processes = []


        p1 = multiprocessing.Process(
            target=self.download_worker,
            args=(logs,)
        )


        p2 = multiprocessing.Process(
            target=self.analysis_worker,
            args=(logs,)
        )


        p3 = multiprocessing.Process(
            target=self.database_worker,
            args=(logs,)
        )


        processes.extend(
            [p1, p2, p3]
        )


        for p in processes:
            p.start()
            p.join()
            



        total = time.time() - start


        logs.append("End")
        logs.append(
            f"{total:.2f} seconds"
        )


        return list(logs)
    


    def naming_scenario_1(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        start = time.time()

        process_with_name = multiprocessing.Process(
            name='myFunc process',
            target=self.naming_worker
        )

        process_with_default_name = multiprocessing.Process(
            target=self.naming_worker
        )

        process_with_name.start()
        process_with_default_name.start()

        process_with_name.join()
        process_with_default_name.join()

        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return list(self.logs)
    
    def naming_scenario_2(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        start = time.time()

        # تعریف فرآیندها با نام‌های خاص
        p1 = multiprocessing.Process(
            name="adder",
            target=self.adder_worker,
            args=([10, 20, 30, 40], self.logs)
        )

        p2 = multiprocessing.Process(
            name="randomizer",
            target=self.randomizer_worker,
            args=(self.logs,)
        )

        p3 = multiprocessing.Process(
            name="reverser",
            target=self.reverser_worker,
            args=("Meysam", self.logs)
        )

        processes = [p1, p2, p3]

        for p in processes:
            p.start()
            p.join()

        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return list(self.logs)

    def naming_scenario_3(self):
        manager = multiprocessing.Manager()
        self.logs = manager.list()
        self.logs.append("The original data is: Meysam")

        start = time.time()

        original_text = "Meysam"
        encrypted_text = "".join(chr(ord(c) + 3) for c in original_text)

        p1 = multiprocessing.Process(
            name="Encryptor",
            target=self.encrypt_worker,
            args=(original_text, self.logs)
        )

        p2 = multiprocessing.Process(
            name="Decryptor",
            target=self.decrypt_worker,
            args=(encrypted_text, self.logs)
        )

        p3 = multiprocessing.Process(
            name="Hasher",
            target=self.hash_worker,
            args=(original_text, self.logs)
        )

        processes = [p1, p2, p3]

        for p in processes:
            p.start()
            p.join()

        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return list(self.logs)



    def background_scenario_1(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        start = time.time()

        background_process = multiprocessing.Process(
            name="background_process",
            target=self.background_mode_worker,
            args=(self.logs,)
        )
        background_process.daemon = True

        foreground_process = multiprocessing.Process(
            name="NO_background_process",
            target=self.background_mode_worker,
            args=(self.logs,)
        )

        foreground_process.daemon = False

        background_process.start()
        foreground_process.start()

        foreground_process.join()

        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return list(self.logs)

    def background_scenario_2(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()
        self.shared_data = manager.dict()
        self.shared_data["last_write"] = "No writes yet"

        start = time.time()

        background_process = multiprocessing.Process(
            name="background_saver",
            target=self.background_saver_worker,
            args=(self.logs, self.shared_data)
        )
        background_process.daemon = True

        writer_process = multiprocessing.Process(
            name="writer_process",
            target=self.writer_worker,
            args=(self.logs, self.shared_data)
        )

        background_process.start()
        writer_process.start()

        writer_process.join()

        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return list(self.logs)
    
    def background_scenario_3(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        start = time.time()

        listener_process = multiprocessing.Process(
            name="listener_process",
            target=self.listener_worker,
            args=(self.logs,)
        )
        listener_process.daemon = True

        sender_process = multiprocessing.Process(
            name="sender_process",
            target=self.sender_worker,
            args=(self.logs,)
        )

        listener_process.start()
        sender_process.start()

        sender_process.join()

        total = time.time() - start

        self.logs.append("End")
        self.logs.append(f"{total:.2f} seconds")

        return list(self.logs)
    
    

    def killing_scenario_1(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        # ساخت فرآیند
        p = multiprocessing.Process(
            name="test_process",
            target=self.foo_worker,
            args=(self.logs,)
        )

        # قبل از اجرا
        self.logs.append(f"Process before execution: {p}, alive={p.is_alive()}")

        # شروع
        p.start()
        self.logs.append(f"Process running: {p}, alive={p.is_alive()}")

        # terminate کردن
        p.terminate()
        self.logs.append(f"Process terminated: {p}, alive={p.is_alive()}")

        # join
        p.join()
        
        self.logs.append(f"Process joined: {p}, alive={p.is_alive()}")
        self.logs.append(f"Process exit code: {p.exitcode}")
        self.logs.append("End")

        return list(self.logs)

    def killing_scenario_2(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()
        self.start_times = manager.dict()

        workers = []

        # ساخت 3 worker
        for i in range(3):
            p = multiprocessing.Process(
                target=self.firstWorker,
                name=f"worker_process_{i+1}",
                args=(self.logs, i)
            )
            workers.append(p)

        # شروع همه workerها
        for i, p in enumerate(workers):
            self.start_times[p.name] = time.time()
            p.start()

        # supervisor
        while True:
            alive_count = 0

            for p in workers:
                if p.is_alive():
                    alive_count += 1
                    elapsed = (time.time() - self.start_times[p.name])-1

                    if elapsed > 5:
                        p.terminate()
                        p.join()
                        self.logs.append(
                            f"{p.name}: killed by supervisor because it took more than 5 secs"
                        )

            if alive_count == 0:
                break

            time.sleep(0.2)

        # چاپ نتیجهٔ نهایی
        for p in workers:
            if p.exitcode == 0:
                self.logs.append(f"{p.name}: finished in normal time")
            else:
                self.logs.append(f"{p.name}: exitcode {p.exitcode}")

        self.logs.append("End")
        return list(self.logs)
    
    def killing_scenario_3(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        workers = []

        
        for i in range(3):
            p = multiprocessing.Process(
                target=self.secondWorker,
                name=f"process_{i+1}",
                args=(self.logs, i)
            )
            workers.append(p)

        # شروع همه
        for p in workers:
            p.start()

        # دو فرایند اول → نرمال (join می‌شوند)
        workers[0].join()
        workers[1].join()

        # فرایند سوم → زامبی (عمداً join نمی‌شود)

        # ---------------- supervisor ----------------

        for p in workers:
            if p.is_alive():
                p.terminate()
                p.join()
                self.logs.append(f"{p.name} killed because it was zombie")
            else:
                # نرمال است
                self.logs.append(f"{p.name} is not zombie")

        self.logs.append("End")
        return list(self.logs)
    


    def subclass_scenario_1(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        processes = []

        for i in range(1, 11):
            p = MyProcess(self.logs, i)
            processes.append(p)

        
        for p in processes:
            p.start()
            p.join()
        

        self.logs.append("End")
        return list(self.logs)

    def subclass_scenario_2(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        numbers = [3, 5, 7, 9]
        processes = []

        
        for i, num in enumerate(numbers, start=1):
            p = SquareProcess(self.logs, num, i)
            processes.append(p)

        
        for p in processes:
            p.start()

        
        for p in processes:
            p.join()

        self.logs.append("End")
        return list(self.logs)
    
    def subclass_scenario_3(self):


        manager = multiprocessing.Manager()
        self.logs = manager.list()

        messages = [
            "loading user data",
            "connecting to server",
            "processing request",
            "saving results",
            "finalizing"
        ]

        processes = []

        
        for i, msg in enumerate(messages, start=1):
            delay = random.randint(1, 5)
            p = MessageProcess(self.logs, msg, delay, i)
            processes.append(p)

        
        for p in processes:
            p.start()

        
        for p in processes:
            p.join()

        self.logs.append("End")
        return list(self.logs)
    


    def queue_scenario_1(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        queue = multiprocessing.Queue()

        producer = Producer(self.logs, queue)
        consumer = Consumer(self.logs, queue)

        producer.start()
        consumer.start()

        producer.join()
        consumer.join()

        self.logs.append("End")
        return list(self.logs)
    
    def queue_scenario_2(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        main_queue = multiprocessing.Queue(maxsize=5)
        worker_queues = [multiprocessing.Queue() for _ in range(3)]

        
        busy_flags = manager.list([False, False, False])

        maker = JobMaker(self.logs, main_queue)
        dispatcher = Dispatcher(self.logs, main_queue, worker_queues, busy_flags)

        processors = [
            Processor(self.logs, worker_queues[i], busy_flags, i+1)
            for i in range(3)
        ]

        maker.start()
        dispatcher.start()

        for p in processors:
            p.start()

        maker.join()

        dispatcher.terminate()
        for p in processors:
            p.terminate()

        self.logs.append("End")
        return list(self.logs)
    
    def queue_scenario_3(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        # صف با ظرفیت محدود
        queue = multiprocessing.Queue(maxsize=10)

        sender = Sender(self.logs, queue)
        receiver = Receiver(self.logs, queue)

        sender.start()
        receiver.start()

        sender.join()

        
        receiver.terminate()

        self.logs.append("End")
        return list(self.logs)



    def pipe_scenario_1(self):

        manager = multiprocessing.Manager()

        self.logs = manager.list()

        pipe_1 = multiprocessing.Pipe(duplex=True)

        pipe_2 = multiprocessing.Pipe(duplex=True)

        producer = ProducerPipe(
            self.logs,
            pipe_1
        )

        square = SquarePipe(
            self.logs,
            pipe_1,
            pipe_2
        )

        producer.start()

        square.start()

        
        pipe_1[0].close()

        pipe_2[0].close()

        try:

            while True:

                value = pipe_2[1].recv()

                self.logs.append(
                    f"Main received {value}"
                )

        except EOFError:

            self.logs.append(
                "Pipe closed"
            )

        producer.join()

        square.join()

        self.logs.append("End")

        return list(self.logs)
    
    def pipe_scenario_2(self):

        manager = multiprocessing.Manager()

        self.logs = manager.list()

        pipe_1 = multiprocessing.Pipe(True)

        pipe_2 = multiprocessing.Pipe(True)

        producer = StringProducer(
            self.logs,
            pipe_1
        )

        reverser = ReverseString(
            self.logs,
            pipe_1,
            pipe_2
        )

        producer.start()

        reverser.start()

        pipe_1[0].close()

        pipe_2[0].close()

        try:

            while True:

                result = pipe_2[1].recv()

                self.logs.append(
                    f"Main received '{result}'"
                )

        except EOFError:

            self.logs.append("Pipe closed")

        producer.join()

        reverser.join()

        self.logs.append("End")

        return list(self.logs)
    
    def pipe_scenario_3(self):

        manager = multiprocessing.Manager()

        self.logs = manager.list()

        pipe_1 = multiprocessing.Pipe(True)

        pipe_2 = multiprocessing.Pipe(True)

        producer = NumberProducer(
            self.logs,
            pipe_1
        )

        factorial = FactorialProcess(
            self.logs,
            pipe_1,
            pipe_2
        )

        producer.start()

        factorial.start()

        pipe_1[0].close()

        pipe_2[0].close()

        try:

            while True:

                result = pipe_2[1].recv()

                self.logs.append(
                    f"Main received {result}"
                )

        except EOFError:

            self.logs.append(
                "Pipe closed"
            )

        producer.join()

        factorial.join()

        self.logs.append("End")

        return list(self.logs)
      


    def pool_scenario_1(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        inputs = list(range(0, 100))

        pool = multiprocessing.Pool(processes=4)

        results = pool.map(WorkerPool.function_square, inputs)

        pool.close()
        pool.join()

        formatted = f"Pool : {results}"
        self.logs.append(formatted)

        self.logs.append("End")

        return list(self.logs)
    
    def pool_scenario_2(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        # لیست پسوردها
        passwords = [
            "pass123",
            "hello2024",
            "admin",
            "mypassword",
            "test123",
            "secret",
            "123456",
            "qwerty",
            "letmein",
            "pythonrocks"
        ]


        # ساخت Pool با 4 پردازش
        pool = multiprocessing.Pool(processes=4)


        # اجرای موازی هش کردن
        hashed_results = pool.map(
            HashWorker.hash_password,
            passwords
        )


        pool.close()
        pool.join()


        # ذخیره خروجی
        formatted = f"Pool Hashes : {hashed_results}"

        self.logs.append(formatted)

        self.logs.append("End")


        return list(self.logs)
    
    def pool_scenario_3(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()


        files_content = [
            "Python is a powerful programming language",
            "Multiprocessing allows parallel execution in Python",
            "Artificial intelligence and machine learning are growing fast",
            "Data science uses Python for data analysis",
            "Deep learning models require powerful computation"
        ]


        pool = multiprocessing.Pool(processes=3)


        results = pool.map(
            FileWorker.count_words,
            files_content
        )


        pool.close()
        pool.join()


        # هر خروجی در یک خط جدا
        self.logs.append("Pool Word Count Results:")

        for index, result in enumerate(results, start=1):

            self.logs.append(
                f"File {index} -> Text: {result['text']} | "
                f"Word Count: {result['word_count']}"
            )


        self.logs.append("End")


        return list(self.logs)



    def barrier_scenario_1(self):

        manager = multiprocessing.Manager()

        self.logs = manager.list()


        synchronizer = multiprocessing.Barrier(2)

        serializer = multiprocessing.Lock()


        p1 = BarrierWorker(
            self.logs,
            synchronizer,
            serializer,
            True
        )

        p1.name = "p1 - with_barrier"


        p2 = BarrierWorker(
            self.logs,
            synchronizer,
            serializer,
            True
        )

        p2.name = "p2 - with_barrier"



        p3 = BarrierWorker(
            self.logs,
            synchronizer,
            serializer,
            False
        )

        p3.name = "p3 - without_barrier"



        p4 = BarrierWorker(
            self.logs,
            synchronizer,
            serializer,
            False
        )

        p4.name = "p4 - without_barrier"



        p1.start()
        p2.start()
        p3.start()
        p4.start()



        p1.join()
        p2.join()
        p3.join()
        p4.join()


        self.logs.append("End")


        return list(self.logs)

    def barrier_scenario_2(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        barrier = multiprocessing.Barrier(4)
        lock = multiprocessing.Lock()

        images = [
            "image1.jpg",
            "image2.jpg",
            "image3.jpg",
            "image4.jpg"
        ]

        processes = []

        for img in images:

            p = multiprocessing.Process(
                target=BarrierImageWorker.image_processing,
                args=(barrier, lock, self.logs, img)
            )

            p.name = img
            processes.append(p)

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        self.logs.append("End")

        return list(self.logs)
    
    def barrier_scenario_3(self):

        manager = multiprocessing.Manager()
        self.logs = manager.list()

        barrier = multiprocessing.Barrier(4)
        lock = multiprocessing.Lock()

        courses = [
            "Math",
            "Physics",
            "Programming",
            "Database"
        ]

        processes = []

        for course in courses:

            p = multiprocessing.Process(
                target=BarrierAverageWorker.calculate_scores,
                args=(barrier, lock, self.logs, course)
            )

            p.name = course

            processes.append(p)

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        self.logs.append("End")

        return list(self.logs)