#!/usr/bin/env bash
ln -f celery.service /etc/systemd/system/celery.service;
systemctl daemon-reload;
systemctl restart celery.service;