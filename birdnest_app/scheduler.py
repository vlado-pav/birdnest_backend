from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import time
import requests
import xmltodict


def tick():
    r = requests.get('https://assignments.reaktor.com/birdnest/drones')
    response = xmltodict.parse(r.content)['report']['capture']['drone'][0]['serialNumber']
    print(response)


    print('Tick! The time is %s' %datetime.now())
    print(scheduler.get_jobs()[0])

if __name__ == '__main__':
    scheduler  = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=2)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
            # This is here to simulate application activity (which keeps the main thread alive).
        counter = 0
        while True:
            time.sleep(4)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()