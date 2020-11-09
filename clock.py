from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon', hour=22)
def scheduled_job():
    print('This job is run every Monday at 10pm.')

sched.start()
