# mcbbs-thread-crawler
A crawler crawls threads in MCBBS.

LAST UPDATE:

#### [2019-11-3 15:53:58](https://tremblestarman.github.io/minecraft/mcbbs/stats/ "stats")

----

## MAIN SCRIPTS

### crawler.py

Main crawler.
data is stored as json in '/database'.
you can edit this script to enable proxy and chage the range of threads you want to crawl.

```
nohup python -u crawler.py > @.log 2>&1 &
```

(log including banned-tid are stored in '@.log')

### crawler_errorfixer.py

Another crawler to fix banned data from reading '@.log'.

```
nohup python -u crawler_errorfixer.py > nohup.log 2>&1 &
```

### stat_categories.py

get data statistic and store in '/stats'.

### figure.py

generate figures, markdown documents and html in '/img', '/mds' and '/html'.