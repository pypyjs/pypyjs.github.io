import os
import sys
import time
import zlib


def hello_world():
    """
    for copy&paste to:
        http://nmrugg.github.io/LZMA-JS/demos/advanced_demo.html

    same as:
    $ echo "Hello, world." | zlib | hexdump -C | cut -c9-60
      5d 00 00 80 00 ff ff ff  ff ff ff ff ff 00 24 19
      49 98 6f 16 02 8c e8 e6  5b b1 47 f2 01 6a 44 1e
      ff ff 8e bc 00 00


    zlib.compressobj([level[, method[, wbits[, memlevel[, strategy]]]]])

        Returns a compression object, to be used for compressing data streams that won’t fit into memory at once. level is an integer from 0 to 9 controlling the level of compression; 1 is fastest and produces the least compression, 9 is slowest and produces the most. 0 is no compression. The default value is 6.

        method is the compression algorithm. Currently, the only supported value is DEFLATED.

        wbits is the base two logarithm of the size of the window buffer. This should be an integer from 8 to 15. Higher values give better compression, but use more memory. The default is 15.

        memlevel controls the amount of memory used for internal compression state. Valid values range from 1 to 9. Higher values using more memory, but are faster and produce smaller output. The default is 8.

        strategy is used to tune the compression algorithm. Possible values are Z_DEFAULT_STRATEGY, Z_FILTERED, and Z_HUFFMAN_ONLY. The default is Z_DEFAULT_STRATEGY.


    """
    compressed = zlib.compress(bytes("Hello, world.", "ascii"), 9)

    print(repr(compressed))
    print
    print(" ".join(["%02x" % b for b in compressed]))
    print("var data = new Array(%s);" % ",".join(["%i" % b for b in compressed]))

    print(zlib.decompress(compressed))


def zlib_compress_file(filepath, out_path, level):
    print("_"*79)
    out_filename="%s_level%i.deflate" % (os.path.split(filepath)[1], level)
    out_filepath = os.path.join(out_path, out_filename)
    print("Compress '%s' to '%s'..." % (filepath, out_filepath))

    statinfo = os.stat(filepath)
    uncompressed_size = statinfo.st_size

    print("Compress with level=%i - (%s Bytes uncompressed)\n" % (
        level, uncompressed_size
    ))


    with open(filepath, "rb") as source_file:
        with open(out_filepath, "wb") as out_file:
            start_time=time.time()
            out_file.write(
                zlib.compress(source_file.read(), level)
            )

    duration = time.time()-start_time
    print("\ncompression time...: %6.2f sec." % duration)

    statinfo = os.stat(out_filename)
    compressed_size = statinfo.st_size
    print("uncompressed.......: %6.2f MBytes" % (uncompressed_size/1024/1024))
    print("compressed.........: %6.2f MBytes" % (compressed_size/1024/1024))

    percent = (100.0 / uncompressed_size) * compressed_size
    print("compression ratio..: %6.2f %%" % percent)

    return duration, percent





if __name__ == "__main__":
    hello_world()

    zlib_compress_file("pypyjs-release/lib/pypy.vm.js", "./", level=9)
    zlib_compress_file("pypyjs-release/lib/pypy.vm.js.mem", "./", level=9)
