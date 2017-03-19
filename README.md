# 4cdl
# A light-weight 4chan image downloader
The downloader will run and download continuously **until 4chan thread dies or being deleted**
## Usage: python 4cdl.py Thread_URL
The command will download json and all image of a 4chan thread into a new folder whose name is the thread_id inside the current directory path.
### More Usage: python 4cdl.py Thread_URL -t number_of_download_thread
The parameter -t specifies number of thread use for download, default is 10


## Feature:
* Multi-threaded downloader
* Resume supported
* Run until thread deleted
