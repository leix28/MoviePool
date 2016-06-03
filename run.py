#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webserver
import logging
import config

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,\
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',\
        datefmt='%m-%d %H:%M')
    webserver.app.config.from_object('config.BasicConfig')
    webserver.app.run()
