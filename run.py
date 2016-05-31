#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webserver
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,\
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',\
        datefmt='%m-%d %H:%M')
    webserver.app.run(debug=True)
