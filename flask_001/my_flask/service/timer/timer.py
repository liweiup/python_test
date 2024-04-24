from flask import Flask
from flask_apscheduler import APScheduler
import datetime

class Timer(object):
    SCHEDULER_API_ENABLED = True
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(port=8000)
    # interval examples
    @scheduler.task('interval', id='do_job_1', seconds=1, misfire_grace_time=900)

    def job1():
        print(str(datetime.datetime.now()) + ' Job 1 executed')

# # cron examples
# @scheduler.task('cron', id='do_job_2', minute='*')
# def job2():
#     print(str(datetime.datetime.now()) + ' Job 2 executed')

# @scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
# def job3():
#     print(str(datetime.datetime.now()) + ' Job 3 executed')


# @scheduler.task('cron', id='do_job_3', day='*', hour='13', minute='26', second='05')
# def job4():
#     print(str(datetime.datetime.now()) + ' Job 4 executed')
