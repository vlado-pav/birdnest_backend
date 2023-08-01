#https://stackoverflow.com/questions/11654353/how-to-setup-apscheduler-in-a-django-project

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from birdnest_app.db_updaters import update_databases
""" 
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', seconds=2, name='auto_hello')
    def auto_hello():
        update_databases() 
    
    scheduler.start() 
"""
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_databases, 'interval', seconds=2)
    scheduler.start()
