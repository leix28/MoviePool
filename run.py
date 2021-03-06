#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webserver
import logging
import os, pwd
import config

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,\
        filename='moviepool.log',\
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',\
        datefmt='%m-%d %H:%M')
    webserver.app.config.from_object('config.BasicConfig')
    if webserver.app.config['NO_FASTCGI']:
        webserver.app.run(host='0.0.0.0')
    else:
        uid = pwd.getpwnam('www-data')[2]
        os.setuid(uid)
        from flup.server.fcgi import WSGIServer
        WSGIServer(webserver.app, bindAddress=webserver.app.config['FASTCGI_SOCK']).run()
