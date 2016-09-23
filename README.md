A small Python 3 module that scans a page and returns dead links

API aerial view {In progress} [![Code Health](https://landscape.io/github/Fuchida/vamp/master/landscape.svg?style=flat)](https://landscape.io/github/Fuchida/vamp/master)
--------------

```Python
from vamp import Vamp

# Setup
crawler = Vamp('http://webpage.com')

# Scan a page or configured site
# if specific page is not specified, index page will be scanned
crawler.scan()

# When a dead link/s is found
>> {"http://example.com/hello.html":404}

# When no dead link/s are found
>> {}

```
