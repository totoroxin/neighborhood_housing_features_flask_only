# Steps to deploy the flask app using bokeh server on AWS


### Create an instance on AWS
reference: https://www.twilio.com/blog/deploy-flask-python-app-aws

### Connect to the virtual machine through SSH

##### start ssh-agent
```
eval ssh-agent -s
```

##### In terminal under directory with the key file `<PROJECT_PEM_NAME>.pem` generated in AWS.
```
chmod 600 <PROJECT_PEM_NAME>.pem
ssh-add <PROJECT_PEM_NAME>.pem
ssh ubuntu@<PROJECT_PUBLIC_IP_ADDRESS>
```
or
```
chmod 600 <PROJECT_PEM_NAME>.pem
ssh -i VUN.pem ubuntu@3.130.17.76
```

Note: the above steps can be replaced by using **PuTTY** to connect to AWS host in Windows

(Download and install PuTTY software on your local computer. Use PuTTYgen to convert your PEM key file to RSA format. Later, you only need RSA key)

### Transfer the project files to VM
You can use three ways to do so: 1) pull Github project repository, 2) copy the app folder from the local path to the remote host in bash, or 3) install **WinSCP** to copy the local app folder to AWS host in Windows

##### Example of the second way to transfer the app folder
Make a new directory in VM
```
mkdir appfolder
```

Transfer the local app folder to the new directory you have just created
```
sudo rsync -rv <FULL_PATH>/ ubuntu@<PROJECT_IP_ADDRESS>:/home/ubuntu/appfolder
```

### Build the environment inside the ubuntu VM on AWS
```
sudo apt update
sudo apt install python3 python3-pip htop
```

If you have a requirements.txt file in your app folder, you can directly install all the packages required by your app through:
```
pip3 install -r requirements.txt
```

### Nginx for reverse the proxy to add bokeh server port
Let 80 port and transfer to 8080 and 5006 (bokeh port) in AWS machine using Nginx
Reference: https://www.hostinger.com/tutorials/how-to-set-up-nginx-reverse-proxy/

Install Nginx in VM
```
sudo apt-get update
sudo apt-get install nginx
```

Disable the Default Virtual Host
```
sudo unlink /etc/nginx/sites-enabled/default
```

Create the Nginx Reverse Proxy
```
cd /etc/nginx/sites-available/

sudo vi reverse-proxy.conf

server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8080;
    }
    location /bokeh/ {
        proxy_pass http://127.0.0.1:5006;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
    location /static/js/bokeh {
        proxy_pass http://127.0.0.1:5006;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}

sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
```

Test and Restart Nginx
```
service nginx configtest
sudo service nginx restart
```

### Create an Elastic IP
For permanently access the web app on AWS from the same IP, we will need to allocate a static address.

Under EC2 Dashboard/Network & Security/Elastic IPs, click ‘Allocate new address’

Under Action/Associate address, choose your EC2 instance and private IP


### Run the app in VM in the background
<PROJECT_NAME>.py is app.py in this directory
```
nohup python <PROJECT_NAME>.py 2>log.err 1>log.out &
```

### Close the app in VM
check and get the app process id
```
ps aux | grep <PROJECT_NAME>.py
```

```
kill [process id]
```
or enforced close, SIGKILL
```
kill -9 [process id]
```

### Update files from github
```
git pull --rebase
```