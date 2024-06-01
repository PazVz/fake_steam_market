[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/fake_steam_market
ExecStart=/root/fake_steam_market/venv/bin/gunicorn --workers 3 --bind unix:/root/fake_steam_market/project.sock project.wsgi:application

[Install]
WantedBy=multi-user.target