#VERSION: 2.00

# Author:
#  Fabien Devaux <fab AT gnux DOT info>
# Contributors:
#  Davide Depau <davide@depau.eu> (Python2+3 support)
#  Christophe Dumez <chris@qbittorrent.org> (qbittorrent integration)
#  Thanks to gab #gcu @ irc.freenode.net (multipage support on PirateBay)
#  Thanks to Elias <gekko04@users.sourceforge.net> (torrentreactor and isohunt search engines)
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

from __future__ import print_function, unicode_literals, division

import argparse
import io
from os import path
from glob import glob
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
import requests
import sys
from . import importer

THREADED = True
try:
    MAX_THREADS = cpu_count()
except NotImplementedError:
    MAX_THREADS = 1

CATEGORIES = {'all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books'}

class Progress:
    def __init__(self, engines_num, is_display):
        self.progress = 0
        self.engines_num = engines_num

        if not is_display:
            self.inc = lambda: None
            self.print = lambda: None

    @staticmethod
    def print(num):
        print("progress={}%".format(num))

    def inc(self):
        self.progress += int(1./self.selected_engines*100)
        self.print(self.progress)

# This ugly workaround will try to mask changes in python2/3 naming conventions
importer.alias_modules()
################################################################################
# Every engine should have a "search" method taking
# a space-free string as parameter (ex. "family+guy")
# it should call prettyPrinter() with a dict as parameter.
# The keys in the dict must be: link,name,size,seeds,leech,engine_url
# As a convention, try to list results by decreasing number of seeds or similar
################################################################################

def get_engines(searchdirs=None):
    """ Import available engines

        Return dict of available engines
    """
    if searchdirs is not None:
        searchdirs = [path.join(path.dirname(__file__), 'engines'),
                      path.join(path.dirname(__file__), '..', 'engines')]

    supported_engines = {}

    for searchdir in searchdirs:
        engines = glob(path.join(searchdir, '*.py'))
        for engine in engines:
            engi = path.basename(engine).split('.')[0].strip()
            if len(engi) == 0 or engi.startswith('_'):
                continue
            try:
                #import engines.[engine]
                engine_module = importer.import_file(engi, engine)
                #get low-level module
                # engine_module = getattr(engine_module, engi)
                #bind class name
                globals()[engi] = getattr(engine_module, engi)
                supported_engines[engi] = engine_module
            except Exception:
                pass

    return supported_engines

def initialize_engines(searchdir=None):
    return list(get_engines(searchdir).keys())

def engines_to_xml(supported_engines):
    """ Generates xml for supported engines """
    tab = " " * 4

    for short_name in supported_engines:
        search_engine = globals()[short_name]()

        supported_categories = ""
        if hasattr(search_engine, "supported_categories"):
            supported_categories = " ".join((key for key in search_engine.supported_categories.keys()
                                             if key is not "all"))

        yield "".join((tab, "<", short_name, ">\n",
                       tab, tab, "<name>", search_engine.name, "</name>\n",
                       tab, tab, "<url>", search_engine.url, "</url>\n",
                       tab, tab, "<categories>", supported_categories, "</categories>\n",
                       tab, "</", short_name, ">\n"))

def displayCapabilities(supported_engines):
    """
    Display capabilities in XML format
    <capabilities>
      <engine_short_name>
        <name>long name</name>
        <url>http://example.com</url>
        <categories>movies music games</categories>
      </engine_short_name>
    </capabilities>
    """
    xml = "".join(("<capabilities>\n",
                   "".join(engines_to_xml(supported_engines)),
                   "</capabilities>"))
    print(xml)

def unbuffer_stdout():
    binstdout = io.open(sys.stdout.fileno(), 'wb', 0)
    sys.stdout = io.TextIOWrapper(binstdout, encoding="UTF-8")

def run_search(engine_list):
    """ Run search in engine
        @param engine_list List with engine, query and category

        @retval False if any exceptions occurred
        @retval True  otherwise
    """
    global progress

    engine, what, cat = engine_list
    try:
        engine = engine()
        # avoid exceptions due to invalid category
        if hasattr(engine, 'supported_categories'):
            cat = cat if cat in engine.supported_categories else "all"
            engine.search(what, cat)
        else:
            engine.search(what)

        # global
        progress.inc()

        return True
    except Exception:
        return False

def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Searches various bittorrent websites and prints out the results in a machine-readable fashion")
    parser.add_argument('--capabilities', default=False, action='store_true',
                        help='Outputs an XML showing search engine plugins capabilities and exits')
    parser.add_argument('--progress', '-p', default=False, action='store_true',
                        help='If set, outputs search progress every now and then')
    parser.add_argument('--engines-dir', '-d', default=[path.join(path.dirname(__file__), 'engines')], dest="engines_dirs", action='append',
                        help='Specify custom directory for engine plugins. Default is the engines directory inside of the current script directory and its parent. Can be specified multiple times')
    parser.add_argument('engines', nargs='?', help='Select engines to be used for search, comma-separated, or "all"')
    parser.add_argument('category', nargs='?', help='Select category to be used for search, or "all"')
    parser.add_argument('keywords', nargs='*', help='Search keywords')

    args = parser.parse_args(args)

    if not args.capabilities and not (args.engines and args.category and args.keywords):
        print("You must specify engines, categories and at least one keyword!", file=sys.stderr)
        parser.print_usage(file=sys.stderr)
        exit(1)

    return args

def main(args=None):
    global progress
    args = parse_args(args)
    supported_engines = initialize_engines(args.engines_dirs)

    if args.capabilities:
        displayCapabilities(supported_engines)
        return

    # TODO: describe benefits
    unbuffer_stdout()

    # get only unique engines with set
    engines_list = set(e.lower() for e in args.engines.strip().split(','))

    if 'all' in engines_list:
        engines_list = supported_engines
    else:
        # discard un-supported engines
        engines_list = [engine for engine in engines_list
                        if engine in supported_engines]

    if not engines_list:
        # engine list is empty. Nothing to do here
        return

    # global
    progress = Progress(len(engines_list), args.progress)

    cat = args.category.lower()

    if cat not in CATEGORIES:
        raise SystemExit(" - ".join(('Invalid category', cat)))

    what = requests.utils.quote(' '.join(args.keywords))
    if THREADED:
        # child process spawning is controlled min(number of searches, number of cpu)
        try:
            pool = Pool(min(len(engines_list), MAX_THREADS))
            pool.map(run_search, ([globals()[engine], what, cat] for engine in engines_list))
        finally:
            pool.terminate()
    else:
        # py3 note: map is needed to be evaluated for content to be executed
        all(map(run_search, ([globals()[engine], what, cat] for engine in engines_list)))

    progress.print(100)

if __name__ == "__main__":
    main()
