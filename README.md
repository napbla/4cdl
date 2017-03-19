# 4cdl
# A light-weight 4chan image downloader
The downloader will run and download continuously **until 4chan thread dies or being deleted**
## Install: pip install 4cdl
Or just download the file
## Usage: python 4cdl.py Thread_URL (without pip install)
example: python 4cdl.py http://boards.4chan.org/biz/thread/1874947
## Usage: 4cdl Thread_URL (with pip install)
example: 4cdl http://boards.4chan.org/biz/thread/1874947
The command will download json and all image of a 4chan thread into a new folder whose name is the thread_id inside the current directory path.
## More Usage: python 4cdl.py Thread_URL -t number_of_download_thread
The parameter -t specifies number of thread use for download, default is 10

## Feature:
* Multi-threaded downloader
* Resume supported
* Run until thread deleted
