# 
### 
# @Auther: renjm
 # @Date: 2019-08-11 14:27:47
 # @LastEditTime: 2019-08-11 16:46:34
 # @Description: 
 ###
sudo apt-get install npm
sudo npm install -g n
sudo npm install -g pm2
sudo apt --fix-broken install -y
sudo apt-get install docker.io -y
sudo docker run -p 3306:3306 --name blogmysql -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql
sudo docker run -p 6379:6379 -v $PWD/data:/data  --name blog-redis -d redis redis-server --appendonly yes
sudo docker run  -d -p 8080:8080  --name myjenkins    -v /root/jenkins-home:/root/jenkins_home  jenkins
sudo docker exec -it blogmysql bash
mysql -uroot -p123456
ALTER user 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';  
FLUSH PRIVILEGES; 
exit
exit

sudo git clone https://github.com/johnsmithsren/python-spider-test.git
sudo git clone https://github.com/johnsmithsren/reactBlog.git
sudo git clone https://github.com/johnsmithsren/koa-test.git
cd reactBlog
sudo npm install 
cd ../
cd koa-test
sudo npm install 
cd ../
