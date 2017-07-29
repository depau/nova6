#VERSION: 1.20

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

from __future__ import print_function, unicode_literals

import argparse
import sys
from .helpers import download_file
from .nova6 import get_engines

def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Downloads a torrent from a website and stores it to a temporary file")
    parser.add_argument('--engines-dir', '-d', default=None, dest="engines_dirs", action='append',
                        help='Specify custom directory for engine plugins. Default is the engines directory inside of the current script directory. Can be specified multiple times')
    parser.add_argument('engine_url', nargs=1, default=None, help='The search engine URL returned from nova2')
    parser.add_argument('download_parameter', nargs=1, default=None, help='The download parameter')

    return parser.parse_args(args)

def main(args=None):
    args = parse_args(args)
    engines = get_engines(args.engines_dirs)
    supported_engines = {getattr(engines[engine], engine).url: engines[engine] for engine in engines}

    if args.engine_url[0] not in list(supported_engines.keys()):
        raise SystemExit('This engine_url was not recognized')
    engine = supported_engines[args.engine_url[0]]

    if hasattr(engine, 'download_torrent'):
        engine.download_torrent(args.download_parameter[0])
    else:
        print(download_file(args.download_parameter[0]))
    sys.exit(0)

if __name__ == '__main__':
    main()