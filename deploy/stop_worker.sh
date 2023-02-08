#!/bin/bash
ps aux | grep 'celery' | awk '{print $2}'| xargs kill