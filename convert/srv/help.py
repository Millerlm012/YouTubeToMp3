from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord import SyncWebhook
import chromedriver_autoinstaller

from functools import wraps
from datetime import datetime
import time
import sys

def log(msg):
    print(f'{datetime.now()} - {msg}', file=sys.stdout)
    return

def send_discord_message(msg):
    hook = 'https://discord.com/api/webhooks/1043242131894059058/wn-3vL2pWdXOHyKQX9vvYZy7g7VyFYbWIW9it0_WlNhUN0B0fGwWtcwSOTrtAoS_e90q'
    webhook = SyncWebhook.from_url(hook)
    webhook.send(msg)
    return

def init_chrome_driver(headless=True):
    # NOTE: this works locally but not in container
    # checks if chromedriver is installed, if not - installs and adds to path
    log('Checking chromedriver...')
    try:
        chromedriver_autoinstaller.install()
    except Exception as e:
        log(f'Something went wrong installing the chromedriver!\nException: {e}')
        exit(1)
    log('Chromedriver is good to go!')
    log('Starting chromedriver!')

    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        log(f'Something went wrong initializing the chromedriver!\nException: {e}')
        exit(1)
    return driver

def run_every(sleep_seconds, run_at_start=False):
    def wrapper(func):
        @wraps(func)
        def run_service(*args, **kwargs):
            try:
                log(f'Started "{func.__name__}".')
                if run_at_start == False:
                    time.sleep(sleep_seconds)
                while True:
                    func(*args, **kwargs)
                    time.sleep(sleep_seconds)
            except KeyboardInterrupt:
                log(f'Stopped "{func.__name__}" successfully!')
                exit(0)
        return run_service
    return wrapper