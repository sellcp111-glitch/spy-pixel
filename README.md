# 🔍 Email Spy Pixel
*A basic tracking pixel to track email opens.*

## Overview
Spy pixels, also commonly referred to as web beacons, are small artifacts implemented in applications to gather user information, which could include the User-Agent string, IP address, and if an email is opened etc. A basic method to collect this information is through the use of a 1x1 pixel with an embedded URL through a transparent PNG, GIF, JPG.

This project uses Python Flask to serve a static web page with a `pixel.png` included in the `.../image` directory. When a user opens an email with the embedded spy pixel, the User-Agent string, timestamp, and IP Address are logged to the `spy_pixel_logs.txt` file. This also allows for named images to do better email campaigning.

## Deploy

To deploy this web application, create a basic server using a VPS / cloud provider of choice. Used Amazon EC2 Ubuntu 20.04 LTS in this deployment.

The following services need to be installed on cloud host, use your favorite package manager (`apt-get install`):
- apache2
- libapache2-mod-wsgi-py3
- python-pip
- python 3.8+

This project assumes you are able to set up a basic Amazon EC2 instance. You can also host it on any other linux machine.

### Step 1

Provision a t2.micro Amazon EC2 instance on Ubuntu 20.04.

💡 Make sure to generate or make note of the public/private key pair. A private key will be downloaded by default if you choose to generate one. Also ensure your security group (or cloud firewall) allows HTTP traffic (port 80).

Take note of the Public EC2 DNS domain name (image below).

![Create EC2 Instance](https://github.com/collinsmc23/spy-pixel/blob/main/images/Public%20DNS.png)

### Step 2

Log into the ubuntu instance with the private key using SSH. Alternatively, select the EC2 instance and use the online "Connect Profile."

`ssh -i "my_private_key.pem" ubuntu@ec2-publicDNS.amazonaws.com`

Clone this repository: `git clone https://github.com/collinsmc23/spy-pixel`

![SSH Output](https://github.com/collinsmc23/spy-pixel/blob/main/images/SSH%20EC2.PNG)

### Step 3

Change directories into the `cd ~/spy-pixel/flaskapp`.

In `~/spy-pixel/flaskapp/flaskapp.py` set `path_to_directory` to match the absolute path to the directory you cloned the spy-pixel repo into. For example if it's in your home folder, you might set this: `path_to_directory = "/home/ubuntu"`. If you don't do this, you'll see a lovely page that tells you that you did not in fact do it...

Link the the app directory to site-root defined apache configuration `sudo ln -sT ~/spy-pixel/flaskapp /var/www/html/flaskapp`.

💡 To check if this works use `echo "Hello World!" > index.html`. You should see this message when navigating to ec2-publicDNS.amazonaws.com.

### Step 4

Add the following block below configuration to the `/etc/apache2/sites-enabled/000-default.conf`. Make sure to fix the python path

```
WSGIDaemonProcess flaskapp threads=5 python-path=<PATH TO YOUR PYTHON SITE-PACKAGES DIRECTORY>
WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi
<Directory flaskapp>
    WSGIProcessGroup flaskapp
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>
```
Similar to this image but with the python path specified.
![Apache Config](https://github.com/collinsmc23/spy-pixel/blob/main/images/Apache-config.png)

*Image source: https://jqn.medium.com/deploy-a-flask-app-on-aws-ec2-1850ae4b0d41*
### Step 5

Restart the web service: `sudo service apache2 restart`.

Go to `http://ec2-publicDNS.amazonaws.com/image` to see the 1x1 pixel.

### Step 6

Add this 1x1 pixel as img src HTML to a web page or email.

`<img src ="Http://ec2-publicDNS.amazonaws.com/image" height=1 width=1>`

You can add a sort of campaign ID by adding a `/<ID>` to the end of the link. This will display in the log.

`<img src ="Http://ec2-publicDNS.amazonaws.com/image/<ID>" height=1 width=1>`

### Step 7

Logging can be found at `Http://ec2-publicDNS.amazonaws.com/logging`


**Spy Away (For Learning Purposes only)**

![Spy Dwight](https://github.com/collinsmc23/spy-pixel/blob/main/images/spy.gif )


