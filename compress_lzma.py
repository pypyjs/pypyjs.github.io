import os
import sys
import time


# New in Python 3.3: https://docs.python.org/3/library/lzma.html
import lzma







def HelloWorld1():
    """
    for copy&paste to:
        http://nmrugg.github.io/LZMA-JS/demos/advanced_demo.html

    same as:
    $ echo "Hello, world." | lzma | hexdump -C | cut -c9-60
      5d 00 00 80 00 ff ff ff  ff ff ff ff ff 00 24 19
      49 98 6f 16 02 8c e8 e6  5b b1 47 f2 01 6a 44 1e
      ff ff 8e bc 00 00
    """

    data = lzma.compress(data=bytes("Hello, world.", encoding="ASCII"),
        format=lzma.FORMAT_ALONE, # The legacy .lzma container format.
        check=lzma.CHECK_NONE, # No integrity check like CRC or SHA
        preset=3, # compression level
        filters=None, # custom filter chains
    )

    print(repr(data))
    print
    print(" ".join(["%02x" % b for b in data]))

    print(lzma.decompress(data))


def HelloWorld2():
    """
    for copy&paste to:
        http://nmrugg.github.io/LZMA-JS/demos/advanced_demo.html

    same as:
    $ echo "Hello, world." | lzma | hexdump -C | cut -c9-60
      5d 00 00 80 00 ff ff ff  ff ff ff ff ff 00 24 19
      49 98 6f 16 02 8c e8 e6  5b b1 47 f2 01 6a 44 1e
      ff ff 8e bc 00 00
    """
    lzc = lzma.LZMACompressor(
        format=lzma.FORMAT_ALONE, # The legacy .lzma container format.
        check=lzma.CHECK_NONE, # No integrity check like CRC or SHA
        preset=3, # compression level
        filters=None, # custom filter chains
    )
    data = lzc.compress(bytes("Hello, world.", encoding="ASCII"))
    data += lzc.flush()

    print(repr(data))
    print
    print(" ".join(["%02x" % b for b in data]))

    print(lzma.decompress(data))


def lzma_compress_file1(filepath, out_path, preset):
    print("_"*79)
    out_filename="%s_preset%i.xz" % (os.path.split(filepath)[1], preset)
    out_filepath = os.path.join(out_path, out_filename)
    print("Compress '%s' to '%s'..." % (filepath, out_filepath))

    statinfo = os.stat(filepath)
    uncompressed_size = statinfo.st_size

    print("Compress with preset=%i - (%s Bytes uncompressed)\n" % (
        preset, uncompressed_size
    ))

    lzc = lzma.LZMACompressor(
        format=lzma.FORMAT_ALONE, # The legacy .lzma container format.
        check=lzma.CHECK_NONE, # No integrity check like CRC or SHA
        preset=preset, # compression level
        filters=None, # custom filter chains
    )

    chunk_size=1 + 1024 * 1024

    with open(filepath, "rb") as source_file:
        with open(out_filepath, "wb") as out_file:
            next_update = time.time() + 0.5
            read_bytes = 0
            start_time=time.time()
            while True:
                chunk_data = source_file.read(chunk_size)
                if not chunk_data:
                    raise RuntimeError

                read_bytes += len(chunk_data)
                out_file.write(lzc.compress(chunk_data))

                done = read_bytes >= uncompressed_size

                if done or time.time() > next_update:
                    percent = (100.0 / uncompressed_size) * read_bytes
                    print("\tread %i Bytes - %.1f%%" % (read_bytes, percent))
                    next_update = time.time() + 1

                if done:
                    out_file.write(lzc.flush())
                    break

    duration = time.time()-start_time
    print("\ncompression time...: %6.2f sec." % duration)

    statinfo = os.stat(out_filename)
    compressed_size = statinfo.st_size
    print("uncompressed.......: %6.2f MBytes" % (uncompressed_size/1024/1024))
    print("compressed.........: %6.2f MBytes" % (compressed_size/1024/1024))

    percent = (100.0 / uncompressed_size) * compressed_size
    print("compression ratio..: %6.2f %%" % percent)

    return duration, percent


def lzma_compress_file2(filepath, out_path, preset):
    print("_"*79)
    out_filename="%s_preset%i.lzma" % (os.path.split(filepath)[1], preset)
    out_filepath = os.path.join(out_path, out_filename)
    print("Compress '%s' to '%s'..." % (filepath, out_filepath))

    statinfo = os.stat(filepath)
    uncompressed_size = statinfo.st_size

    print("Compress with preset=%i - (%s Bytes uncompressed)\n" % (
        preset, uncompressed_size
    ))


    with open(filepath, "rb") as source_file:
        with open(out_filepath, "wb") as out_file:
            start_time=time.time()
            out_file.write(
                lzma.compress(data=source_file.read(),
                    format=lzma.FORMAT_ALONE, # The legacy .lzma container format.
                    check=lzma.CHECK_NONE, # No integrity check like CRC or SHA
                    preset=preset, # compression level
                    filters=None, # custom filter chains
                )
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
    # HelloWorld1()
    # HelloWorld2()
    # lzma_compress_file1("pypyjs-release/lib/pypy.vm.js", "./", preset=3)
    # lzma_compress_file1("pypyjs-release/lib/pypy.vm.js.mem", "./", preset=3)

    lzma_compress_file2("pypyjs-release/lib/pypy.vm.js", "./", preset=3)
    lzma_compress_file2("pypyjs-release/lib/pypy.vm.js.mem", "./", preset=3)

    # lzma_compress_file2("pypyjs-release/lib/pypy.vm.js", "./", preset=4)
    # lzma_compress_file2("pypyjs-release/lib/pypy.vm.js.mem", "./", preset=4)
