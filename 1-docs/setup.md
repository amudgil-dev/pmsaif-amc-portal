## setup

pmsportal_aug_2024/
├── app/
│ ├── **init**.py
│ ├── models.py
│ ├── routes.py
│ ├── forms.py
│ ├── extensions.py
│ ├── cli.py # Add this file here
│ └── templates/
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ └── transactions.html
├── bootstrap/
│ └── loaddata.py
├── config.py
├── .env
└── run.py

### Remember to set the FLASK_APP environment variable to point to your application. You can do this by running:

export FLASK_APP=run.py
