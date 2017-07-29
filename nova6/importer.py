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

# Yeah I know
def alias_modules():
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