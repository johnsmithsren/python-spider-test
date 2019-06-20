# python-spider-test
### scrapy 流程 
> 1. spider 类将需要的url传入到engine中，
> 2. 然后 engin传给 调度类schedule中，
> 3. schedule处理一下然后会返回给engine 然后通过engine传送给downloader下载器
> 4. 下载器完成之后，会返回数据给engine 
> 5. engine会返回给 爬虫类spider spider处理结束会返回给engine然后，
> 6. engine会给pipline这边，pipeline存储结束，通知schedule那边
> 7. 然后调度器这边继续重复这个流程