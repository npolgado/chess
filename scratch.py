import threading
import time

class BackgroundClass(threading.Thread):
    def run(self):
        self.i = 0

    def background_function(self):
        # Function to be called without interrupting the main thread
        self.i += 1

    def get_i(self):
        return self.i

# Main script
if __name__ == "__main__":
    # Create an instance of the BackgroundClass
    background_instance = BackgroundClass()

    # Start the background thread
    background_instance.start()

    # Main script continues running
    while True:
        print("Main script is running...")
        time.sleep(2)

        # Call the background function without interrupting the main thread
        background_instance.background_function()

        print(background_instance.get_i())



    