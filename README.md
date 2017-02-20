A small Python 3 module that scans a page and returns dead links
[![Code Health](https://landscape.io/github/Fuchida/vamp/master/landscape.svg?style=flat)](https://landscape.io/github/Fuchida/vamp/master)

### Installation
--------------
```
git clone https://github.com/Fuchida/vamp.git

virtualenv --distribute --no-site-packages vamp -p /path/to/your/python3

. bin/activate

pip install -r requirements.txt

# Debug mode
python vamp http://example.com

```

API aerial view
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
