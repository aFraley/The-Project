#!/usr/bin/env bash
ln -f django-ember_nginx /etc/nginx/sites-enabled/django-ember_nginx
systemctl daemon-reload;
systemctl restart nginx.service;