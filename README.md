# Standalone Novasearch

This is a fork of [qBittorrent's Nova search engine](https://github.com/qbittorrent/qBittorrent/tree/master/src/searchengine).

It has been patched to use modern [requests](http://docs.python-requests.org/en/master/) library, add a setuptools installer for standalone usage and support both Python2 and Python3 out of the box (though this should not be relied upon).

Please note that even though this works on Python2, development will only focus on Python3.

## How to use

* Install it

```shell
$ pip install nova6
```

* Get some engines from qBittorrent: https://github.com/qbittorrent/search-plugins

* Run it

```shell
$ nova6 -d search-plugins all all query
```

## Synopsis

Nova6 tries to maintain command-line compatibility with nova from qBittorrent. However, in order to make it distributable and still maintain compatibility with existing plugins, I had to make some changes.

Notably, `nova6` accepts one extra command line argument that `nova2` does not: `--engines-dir`, `-d`.

This argument can be specified multiple times with a list of directories to be scanned for plugins. If none is specified, it checks for an `engines` in the same directory of `nova6.py`, just like qBittorrent's.

### Positional arguments

* **engines**

    Select the engines to be used for search, comma-separated, or "all". Use `--capabilities` to list available plugins.
    
* **category**
    
    Select the category to be used for search, or "all". Available categories are `movies`, `tv`, `music`, `games`, `anime`, `software`, `pictures` and `books`.
    
* **keywords**

    Search keywords
    
### Optional arguments

* **--capabilities**

    Outputs an XML showing search engine plugins capabilities and exits immediately.
    
* **--engines-dir**, **-d**
    
    See above. Specify custom directory for engine plugins. Can be specified multiple times.

## Output

### Search

Search results are meant to be machine readable. The format is the following:

```link|name|size|seeds|leech|engine_url```


* **link** → a string corresponding the the download link (points to the .torrent file)
* **name** → a unicode string corresponding to the torrent's name (i.e: "Ubuntu Linux 17.04")
* **size** → a string corresponding to the torrent size (i.e: "6 MB" or "200 KB" or "1.2 GB"...)
* **seeds** → the number of seeds for this torrent
* **leech** → the number of leechers for this torrent
* **engine_url** → the search engine url (i.e: http://www.mininova.org)
* **desc_link** (optional) → if the search plugin provides it, a human-readable page describing the torrent


### Capabilities

Outputs an XML listing all the engines found in search directories and their capabilities. For example:

```xml
<capabilities>
    <myengine>
        <name>My Super Torrent Engine</name>
        <url>https://www.mytorrentengine.com</url>
        <categories>movies anime books software games tv music</categories>
    </myengine>
    ...
</capabilities>
```

## How to write plugins

Please see [qBittorrent's guide](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin).

## Credits and license

All this code has been taken from qBittorrent. It's been adjusted by [Davide Depau](https://github.com/Depaulicious) to make it standalone and reusable.

The license is the same as qBittorrent, GPLv2.
