import bencode, hashlib, StringIO
from deluge_client.client import DelugeRPCClient,ConnectionLostException,CallTimeoutException
import logging
import base64

import crawler
from webserver import app

def initDownloader():
    global client
    logging.info("initDownloader")
    DelugeRPCClient.timeout=6
    client = DelugeRPCClient(app.config['DELUGE_HOST'], 58846, app.config['DELUGE_USER'], app.config['DELUGE_PASSWD'])
    client.connect()
    logging.info("connected={}".format(client.connected))


def getTorrentHash(torrent_data):
    torrent = bencode.bdecode(torrent_data)
    info=torrent['info']
    return hashlib.sha1(bencode.bencode(info)).hexdigest()

def startNewDownload(ByrId):
    torrent = crawler.getByrTorrent(ByrId)    
    if torrent is None:
        return (False, None)
    thash = getTorrentHash(torrent)
    if not client.connected:
        initDownloader()
    ret = ''
    try:
        logging.info('New download {}'.format(ByrId))
        ret = client.call('core.add_torrent_file', '', base64.b64encode(torrent), {})
        logging.debug(ret)
    except ConnectionLostException, e:
        logging.warning("ConnectionLostException")
        client.connected = False

    return (ret==thash, thash)

def getOfflineDownloadPath(bt_hash):
    if not client.connected:
        initDownloader()
    ret = None
    try:
        ret = client.call('core.get_torrents_status', {'hash': bt_hash}, ['files'])
        logging.debug(ret)
    except ConnectionLostException, e:
        logging.warning("ConnectionLostException")
        client.connected = False
    if ret and ret.has_key(bt_hash):
        f = max(ret[bt_hash]['files'], key=lambda t: t['size'])
        return app.config['OFFLINE_DOWNLOADED_PATH']+f['path']
    return None

def getDownloadStatusEach(entries):
    query = []
    for item in entries:
        if item['bt_hash']:
            query.append(item['bt_hash'])
            item['progress'] = -1
            item['finished'] = False
        else:
            item['progress'] = -1
            item['finished'] = False
    if not client.connected:
        initDownloader()
    ret = {}
    try:
        ret = client.call('core.get_torrents_status', {'hash': query}, ['is_finished','progress'])
        logging.debug(ret)
    except ConnectionLostException, e:
        logging.warning("ConnectionLostException")
        client.connected = False

    for item in entries:
        if item['bt_hash'] and ret.has_key(item['bt_hash']):
            item['progress'] = ret[item['bt_hash']]['progress']
            item['finished'] = ret[item['bt_hash']]['is_finished']

