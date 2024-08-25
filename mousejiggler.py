import time
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--hours", type=int, default=0)
parser.add_argument("--minutes", type=int, default=0)
parser.add_argument("-l", "--long", action="store_true",
                    help="Jiggle once every 5 minutes")
args = parser.parse_args()

time_to_run_s = 0
time_to_run_s += args.hours*3600
time_to_run_s += args.minutes*60

start_time = datetime.datetime.now()
time_to_finish = start_time + datetime.timedelta(0,time_to_run_s) # days, seconds, then other fields.

if time_to_run_s != 0:
    print(f"Jiggling for {args.hours} hours and {args.minutes} minutes.\n" 
          f"Current system time is {start_time.strftime('%H:%M:%S')}\n"
          f"Jiggling will stop at {time_to_finish.strftime('%H:%M:%S')}")
else:
    print(f"No time provided - jiggling indefinitely. Ctrl-C to kill the program. Current system time is {start_time.strftime('%H:%M:%S')}.")

if args.long:
    print(f"-l flag passed - jiggling at an interval of 5 minutes.")

# get current mouse position and assign to variables
while True:
    x, y = pyautogui.position()

    curr_time = datetime.datetime.now()
    delta_t = curr_time - start_time
    tsecs = delta_t.total_seconds()
    if time_to_run_s != 0:
        if tsecs > time_to_run_s:
            break
    #pyautogui.moveTo(100, 100, duration = 1)
    pyautogui.moveTo(x, y+1, duration = 0.1)

    x, y = pyautogui.position()

    #pyautogui.moveTo(200, 100, duration = 1)
    pyautogui.moveTo(x, y-1, duration = 0.1)

    if args.long:
        time.sleep(300)
    else:
        time.sleep(10)```