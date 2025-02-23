import time
import os
from datetime import datetime

#START
start_time = time.time()
start_datetime = datetime.now()

SCRIPT_PATH = os.path.abspath(__file__).replace('\\', '/')
MODEL_TO_RUN_PATH = SCRIPT_PATH.replace("/runner.py", "/model.py")
MODEL_ACCURACY_PATH = SCRIPT_PATH.replace("/runner.py", "/modelAccuracy.py")
slash_positions = [pos for pos, char in enumerate(SCRIPT_PATH) if char == '/']
MODEL_PATH = SCRIPT_PATH[:slash_positions[-1]]
SCRIPT_PATH = SCRIPT_PATH[:slash_positions[-8]] + '/'
MODEL_PATH = MODEL_PATH[slash_positions[6]:]

with open(SCRIPT_PATH + "running.txt", "a", encoding="utf-8") as f:
    f.write("\n")
    f.write(MODEL_PATH + " running...\n")
    print(MODEL_PATH + " running...")
    f.write(f"Started running at time: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"Started running at time: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

with open(MODEL_TO_RUN_PATH) as f:
    try:
        exec_globals = {
            '__file__': os.path.abspath(MODEL_TO_RUN_PATH)
        }
        exec(f.read(), exec_globals)
    except SystemExit:
        print("All updated...")

with open(MODEL_ACCURACY_PATH) as f:
    try:
        exec_globals = {
            '__file__': os.path.abspath(MODEL_ACCURACY_PATH)
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
with open(SCRIPT_PATH + "running.txt", "a", encoding="utf-8") as f:
    f.write(f"Ended running at time: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"Ended running at time: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    f.write(f"Program executed in {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds\n")
    print(f"Program executed in {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds")