A small Python 3 module that scans a page and returns dead links

API aerial view
=======

```Python
from vamp import Vamp

# Setup
vampScanner = Vamp('http://webpage.com')

# Scan a page
VampScanner.scan()

# When a deal link/s is found
>> {"http://example.com/hello.html":404}

# When no dead link/s are found
>> {}

```
