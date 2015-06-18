
from __future__ import print_function

import os
import sys
import time

import six

import zlib


# New in Python 3.3: https://docs.python.org/3/library/lzma.html
# import lzma


def compress_zopfli(data):
    """
    https://github.com/wnyc/py-zopfli
    https://pypi.python.org/pypi/zopfli
    """
    try:
        from zopfli import zopfli
    except ImportError as err:
        print("Import error:\n%s" % err)
        print("\nPyzopfli not installed?!?")
        print("\ne.g.:")
        print("    pip install zopfli")
        sys.exit(-1)

    return zopfli.compress(data,
        gzip_mode=0
    )


def test_zopfli():
    print("test zopfli...\n")

    data = b"Hello, world."
    print("Compress with zopfli: %r" % data)
    compressed = compress_zopfli(data)

    print("\ncompresed:", repr(compressed))
    print()
    print(" ".join(["%02x" % b for b in six.iterbytes(compressed)]))
    print()
    print("var data = new Array(%s);" % ",".join(["%i" % b for b in six.iterbytes(compressed)]))

    print("\ndecompress with zlib:", zlib.decompress(compressed))


def hello_world():
    """
    for copy&paste to:
        http://nmrugg.github.io/LZMA-JS/demos/advanced_demo.html

    same as:
    $ echo "Hello, world." | zlib | hexdump -C | cut -c9-60
      5d 00 00 80 00 ff ff ff  ff ff ff ff ff 00 24 19
      49 98 6f 16 02 8c e8 e6  5b b1 47 f2 01 6a 44 1e
      ff ff 8e bc 00 00
    """

    compressed = zlib.compress(bytes("Hello, world.", "ascii"), 9)

    print(repr(compressed))
    print
    print(" ".join(["%02x" % b for b in compressed]))
    print("var data = new Array(%s);" % ",".join(["%i" % b for b in compressed]))

    print(zlib.decompress(compressed))


class Zlib(object):
    def __init__(self, level=9):
        self.level = level

    def get_info(self):
        return "zlib level=%i" % self.level

    def compress(self, data):
        return zlib.compress(data, self.level)

    def filename_suffix(self):
        return "_level%i.deflate" % self.level


class Zopfli(object):
    def get_info(self):
        return "zopfli"

    def compress(self, data):
        try:
            from zopfli import zopfli
        except ImportError as err:
            print("Import error:\n%s" % err)
            print("\nPyzopfli not installed?!?")
            print("\ne.g.:")
            print("    pip install zopfli")
            sys.exit(-1)

        return zopfli.compress(data,
            gzip_mode=0, # zlib container
            # gzip_mode=2, # gzip container

            verbose=True, # debugging data to stderr

            numiterations = 15, # Maximum amount of times to rerun forward and
            # backward pass to optimize LZ77 compression cost.
            # Good values: 10, 15 for small files, 5 for files over
            # several MB in size or it will be too slow.
            # Default value: 15.

            blocksplitting = 1, # If true, splits the data in multiple deflate
            # blocks with optimal choice for the block boundaries. Block
            # splitting gives better compression.
            # Default: true (1).

            blocksplittinglast = 0, # If true, chooses the optimal block
            # split points only after doing the iterative LZ77 compression.
            # If false, chooses the block split points first, then does
            # iterative LZ77 on each individual block. Depending on the file,
            # either first or last gives the best compression.
            # Default: false (0).

            blocksplittingmax = 15, #  Maximum amount of blocks to split into
            # (0 for unlimited, but this can give extreme results that hurt
            # compression on some files).
            # Default value: 15.
        )

    def filename_suffix(self):
        return "_zopfli" #% self.level


def compress_file(filepath, out_path, compressor):
    out_filename="%s%s" % (
        os.path.split(filepath)[1],
        compressor.filename_suffix()
    )

    out_filepath = os.path.join(out_path, out_filename)
    src_name = os.path.split(filepath)[1]
    print("\nCompress '%s' with %s to '%s'" % (
        src_name, compressor.get_info(), out_filepath
    ))

    statinfo = os.stat(filepath)
    uncompressed_size = statinfo.st_size

    print("uncompressed.......: %6.2f MBytes" % (uncompressed_size/1024/1024))

    with open(filepath, "rb") as source_file:
        with open(out_filepath, "wb") as out_file:
            start_time=time.time()
            out_file.write(
                compressor.compress(source_file.read())
            )

    duration = time.time()-start_time
    print("compression time...: %6.2f sec." % duration)

    statinfo = os.stat(out_filename)
    compressed_size = statinfo.st_size
    print("compressed.........: %6.2f MBytes" % (compressed_size/1024/1024))

    percent = (100.0 / uncompressed_size) * compressed_size
    print("compression ratio..: %6.2f %%" % percent)

    return duration, percent





if __name__ == "__main__":
    # test_zopfli()
    # hello_world()

    compressors = (
        # Zlib(level=1),
        Zlib(level=9),
        Zopfli(),
    )

    for compressor in compressors:
        print("="*79)
        compress_file("pypyjs-release/lib/pypy.vm.js", "./", compressor)
        compress_file("pypyjs-release/lib/pypy.vm.js.mem", "./", compressor)

    print("="*79)

