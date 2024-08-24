### rsync to ubuntu

rsync -avz -e "ssh -i ~/.ssh/dm_mumbai_aws_key.pem" --exclude '**pycache**' --exclude='vcwk' ~/projects/pms-aif/pmsportal_aug_2024/ ubuntu@52.66.87.168:pmsweb2/

### ssh into remote server

ssh -i "dm_mumbai_aws_key.pem" ubuntu@ec2-52-66-87-168.ap-south-1.compute.amazonaws.com

### Running the app in test- prod using gunicorn

gunicorn --bind 0.0.0.0:5002 wsgi:app

or

gunicorn -w 4 'wsgi:app'

or

gunicorn --workers 4 --bind 0.0.0.0:5002 --log-level info 'wsgi:app'

### Running the app in prod using gunicorn

#### Create a systemd service file: Create a file named /etc/systemd/system/myproject.service with the following content (adjust paths as necessary):

[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=your_username
Group=your_group
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/virtualenv/bin"
ExecStart=/path/to/your/virtualenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target

#### Start and enable the Gunicorn server

sudo systemctl start myproject
sudo systemctl enable myproject
