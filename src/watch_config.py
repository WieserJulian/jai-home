import time
import threading
from pathlib import Path
import subprocess
# import os

CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config.yaml'
RESTART_COMMAND = ['systemctl', '--user', 'restart', 'jai-voice.service']  # adjust as needed

def watch_config(stop_event: threading.Event):
    last_mtime = None
    while not stop_event.is_set():
        try:
            mtime = CONFIG_PATH.stat().st_mtime
            if last_mtime is None:
                last_mtime = mtime
            elif mtime != last_mtime:
                print(f"Config changed, restarting service: {CONFIG_PATH}")
                subprocess.run(RESTART_COMMAND, check=False)
                last_mtime = mtime
        except Exception as e:
            print(f"Error watching config: {e}")
        time.sleep(5)

if __name__ == '__main__':
    stop = threading.Event()
    try:
        watch_config(stop)
    except KeyboardInterrupt:
        stop.set()
