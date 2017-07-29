# VERSION: 1.42

# Author:
#  Christophe DUMEZ (chris@qbittorrent.org)

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals

import re
import tempfile
import os
import sys
import socket
import requests
from . import socks

if sys.version_info.major == 2:
    from htmlentitydefs import name2codepoint
else:
    from html.entities import name2codepoint

# Some sites blocks default python User-agent
user_agent = 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0'
headers = {'User-Agent': user_agent}
# SOCKS5 Proxy support
if "sock_proxy" in os.environ and len(os.environ["sock_proxy"].strip()) > 0:
    proxy_str = os.environ["sock_proxy"].strip()
    m = re.match(r"^(?:(?P<username>[^:]+):(?P<password>[^@]+)@)?(?P<host>[^:]+):(?P<port>\w+)$", proxy_str)
    if m is not None:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, m.group('host'), int(m.group('port')), True, m.group('username'),
                              m.group('password'))
        socket.socket = socks.socksocket


def htmlentitydecode(s):
    # First convert alpha entities (such as &eacute;)
    # (Inspired from http://mail.python.org/pipermail/python-list/2007-June/443813.html)
    def entity2char(m):
        entity = m.group(1)
        if entity in name2codepoint:
            return chr(name2codepoint[entity])
        return " "  # Unknown entity: We replace with a space.

    t = re.sub('&(%s);' % '|'.join(name2codepoint), entity2char, s)

    # Then convert numerical entities (such as &#233;)
    t = re.sub('&#(\d+);', lambda x: chr(int(x.group(1))), t)

    # Then convert hexa entities (such as &#x00E9;)
    return re.sub('&#x(\w+);', lambda x: chr(int(x.group(1), 16)), t)


def retrieve_url(url):
    """ Return the content of the url page as a string """
    r = requests.get(url, headers=headers)
    dat = r.text
    dat = htmlentitydecode(dat)
    return dat


def download_file(url, referer=None):
    """ Download file at url and write it to a file, return the path to the file and the url """
    # Download url
    headers = globals()["headers"]
    if referer is not None:
        headers['referer'] = referer
    r = requests.get(url, headers=headers)
    dat = r.content

    # Write it to a file
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
        f.write(dat)

    # return file path
    return path + " " + url
