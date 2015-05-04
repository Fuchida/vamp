A small Python 3 module that scans a page and returns dead links

API aerial view
=======

```Python
from vamp import Vamp

# Setup
vamp_scanner = Vamp('http://webpage.com')

# Scan a page
# if specific page is not specified, index page will be scanned
vamp_scanner.page_deadlinks()

# When a deal link/s is found
>> {"http://example.com/hello.html":404}

# When no dead link/s are found
>> {}

```
