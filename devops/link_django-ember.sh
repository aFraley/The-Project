#!/usr/bin/env bash
ln -f django-ember.service /etc/systemd/system/django-ember.service;
systemctl daemon-reload;
systemctl restart django-ember.service;