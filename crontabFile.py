from crontab import CronTab

my_cron = CronTab(user='rjm1149104294')
my_cron.remove_all()
job = my_cron.new(command='sudo /usr/bin/python /scrapy/python-spider-test/begin.py > /temp.log')
job.minutes.every(10)
my_cron.write()
job2 = my_cron.new(command='sudo /usr/bin/python /scrapy/python-spider-test/sendMail.py > /temp.log')
job.minutes.every(15)
my_cron.write()
