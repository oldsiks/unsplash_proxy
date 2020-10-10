

import time
from threading import Thread
from LinkCrawl import DownLink
from ImageCrawl import DownImage
from Proxy import ProxyPool

def main():

    Thread(target=ProxyPool().run).start()
    time.sleep(2)
    Thread(target=DownLink().run).start()
    time.sleep(2)
    for i in range(5):
        x = Thread(target=DownImage().run)
        x.start()


if __name__ == '__main__':
    main()