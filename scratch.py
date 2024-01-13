import threading
import time

class ThreadedClass:
    def __init__(self, name):
        self.name = name
        self.test_bool = True

    def print_numbers(self):
        for i in range(5):
            time.sleep(1)
            print(f"{self.name}: {i} | {self.test_bool}")

    def start_thread(self):
        thread = threading.Thread(target=self.print_numbers)
        thread.start()

# Example usage
if __name__ == "__main__":
    obj1 = ThreadedClass("Thread 1")
    obj2 = ThreadedClass("Thread 2")

    # Start threads
    obj1.start_thread()
    obj2.start_thread()

    # Main thread continues its work
    while True:
        time.sleep(1)
        print(f"Main Thread: {obj1.test_bool} | {obj2.test_bool}")