import time
import os
from datetime import datetime

#START
start_time = time.time()
start_datetime = datetime.now()

print(f"Started running at time: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

with open("modelPredictions.py") as f:
    try:
        exec_globals = {
            '__file__': os.path.abspath('modelPredictions.py')
        }
        exec(f.read(), exec_globals)
    except SystemExit:
        print("All updated...")

#END
total_time = time.time() - start_time
days = total_time // (24 * 3600)
total_time = total_time % (24 * 3600)
hours = total_time // 3600
total_time %= 3600
minutes = total_time // 60
seconds = total_time % 60

end_datetime = datetime.now()

print(f"Ended running at time: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Program executed in {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds")