const cron = require('node-cron');
const { exec } = require('child_process');
const task = cron.schedule('00 30 15 * * *', () =>  {
  // 输出当前目录（不一定是代码所在的目录）下的文件和文件夹
exec('python sendMail.py >> sendMail.log', (err, stdout, stderr) => {
})
}, {
   scheduled: true,
   timezone: "Asia/Shanghai"
});

const task2 = cron.schedule('00 00 15 * * *', () =>  {
  // 输出当前目录（不一定是代码所在的目录）下的文件和文件夹
exec('python begin.py >> run.log', (err, stdout, stderr) => {
})
}, {
  scheduled: true,
   timezone: "Asia/Shanghai"
});

//const task3 = cron.schedule('00 30 15 * * *', () =>  {
//fs.writeFileSync('log.txt', 'gggg \n',{'flag':'a+'}, (err) => {
//    // throws an error, you could also catch it here
//    if (err) throw err;
//});
//}, {
//  scheduled: false
//});
task.start();
task2.start()
//task3.start()
