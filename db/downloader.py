import bencode, hashlib, StringIO
import crawler

def getTorrentHash(torrent_data):
    torrent = bencode.bdecode(torrent_data)
    info=torrent['info']
    return hashlib.sha1(bencode.bencode(info)).hexdigest()

def startNewDownload(ByrId):
    torrent = crawler.getByrTorrent(ByrId)    
    if torrent is None:
        return (False, None)
    #TODO: to deluge

    return (True, getTorrentHash(torrent))


def getDownloadStatusEach(entries):
    for item in entries:
        if item['bt_hash']:
            #TODO from deluge
            item['progress'] = 0
            item['finished'] = False
        else:
            item['progress'] = -1
            item['finished'] = False
