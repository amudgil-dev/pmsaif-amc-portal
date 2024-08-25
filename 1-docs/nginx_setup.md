# open editor

sudo nano /etc/nginx/sites-available/pmsportal

## Add the following configuration:

server {
listen 80;
server_name 13.235.16.153;

    location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

}

# Save and exit the editor.

# Create a symbolic link to enable the site:

sudo ln -s /etc/nginx/sites-available/pmsportal /etc/nginx/sites-enabled/

# Remove the default Nginx configuration:

sudo rm /etc/nginx/sites-enabled/default

# Test the Nginx configuration:

sudo nginx -t

# If the test is successful, reload Nginx:

sudo systemctl reload nginx

# Check Nginx status:

sudo systemctl status nginx
