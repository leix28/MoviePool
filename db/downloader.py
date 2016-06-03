
def getDownloadStatusEach(entries):
    for item in entries:
        if item['bt_hash']:
            item['progress'] = -1
            item['finfished'] = False