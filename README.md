A small Python 3 module that scans a page and returns dead links

API aerial view
=======

```Python
from vamp import Vamp

# Setup
vampScanner = Vamp()

# Scan a page
VampScanner.scan("http://webpage.com")

# When a deal link/s is found
>> {"http://example.com/hello.html":404}

# When no dead link/s are found
>> {}

# HTTP connection fails, an exception is raised by HTTP lib being used

```
