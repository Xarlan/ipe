
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import shodan
import time

import src.ipe_tools.ipe_common as ipe_tools

class IpeRecon(ipe_tools.IpeTools):
    """
    This class realize method to check
    - check SSL/TLS settings using SSlyze library
      documentation: https://nabla-c0d3.github.io/sslyze/documentation/index.html
    - brute force hidden web directory using wfuzz
      documentation: https://github.com/xmendez/wfuzz
    """

    def __init__(self):
        ipe_tools.IpeTools.__init__()
        pass

    def check_ssl_tls(self):
        pass