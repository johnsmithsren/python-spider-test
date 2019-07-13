from crontab import CronTab

my_cron = CronTab(user='renjm')
job = my_cron.new(command='python /Users/renjm/project/scrapy/renjm/')
job.hour.every(24)
my_cron.write()
job2 = my_cron.new(command='python /Users/renjm/project/scrapy/renjm/sendMail.py')
job.hour.every(25)
my_cron.write()