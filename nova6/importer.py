#VERSION: 2.00

# Author:
#  Davide Depau <davide@depau.eu>
#
# Licence: BSD

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

import sys

# https://stackoverflow.com/a/67692/1124621

if sys.version_info.major == 3 and sys.version_info.minor >= 5:
    def import_file(name, path):
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

elif sys.version_info.major == 3 and sys.version_info.minor < 5:
    def import_file(name, path):
        from importlib.machinery import SourceFileLoader
        module = SourceFileLoader(name, path).load_module()
        return module

else:  # Python 2
    def import_file(name, path):
        import imp
        return imp.load_source(name, path)

def alias_modules():
    """
    Creates aliases to nova6 modules and version independent HTML Parser.
    """
    from . import helpers, novaprinter, socks, sgmllib3
    sys.modules["helpers"] = helpers
    sys.modules["novaprinter"] = novaprinter
    sys.modules["socks"] = socks
    sys.modules["sgmllib3"] = sgmllib3

    if sys.version_info.major == 3:
        import html.parser
        import urllib
        import urllib.parse
        sys.modules["HTMLParser"] = sys.modules["html.parser"]
        urllib.urlencode = urllib.parse.urlencode
    else:
        import HTMLParser
        sys.modules["html.parser"] = sys.modules["HTMLParser"]