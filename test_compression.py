from __future__ import print_function

import os
import sys
import time
from pprint import pprint
import zlib
import bz2

# New in Python 3.3: https://docs.python.org/3/library/lzma.html
import lzma


try:
    import creole
    from creole.shared.markup_table import MarkupTable
except ImportError as err:
    print("Import error: %s" % err)
    print("\nMaybe creole not installed?!?")
    print("e.g.:")
    print("    pip install python-creole")
    sys.exit(-1)


class Zlib(object):
    def __init__(self, level=9):
        self.level = level

    def get_info(self):
        return "zlib level=%i" % self.level

    def compress(self, data):
        return zlib.compress(data, self.level)

    def filename_suffix(self):
        return "_level%i.deflate" % self.level


class Bzip2(object):
    def __init__(self, level=9):
        self.level = level

    def get_info(self):
        return "bzip2 level=%i" % self.level

    def compress(self, data):
        return bz2.compress(data, self.level)

    def filename_suffix(self):
        return "_level%i.bz2" % self.level


class Lzma(object):
    def __init__(self, preset=5):
        self.preset = preset

    def get_info(self):
        return "lzma preset=%i" % self.preset

    def compress(self, data):
        return lzma.compress(data,
            format=lzma.FORMAT_ALONE, # The legacy .lzma container format.
            check=lzma.CHECK_NONE, # No integrity check like CRC or SHA
            preset=self.preset, # compression preset
            filters=None, # custom filter chains
        )

    def filename_suffix(self):
        return "_preset%i.lzma" % self.preset


class FileInfo(object):
    def __init__(self, files):
        self.files = files

    def print_table(self):
        print("\n**Uncompressed sizes:**\n")
        print("size in MB | size in Bytes  | file name")
        print("---------- | -------------- | ---------------")
        for file_path in self.files:
            statinfo = os.stat(file_path)
            uncompressed_size = statinfo.st_size
            name = os.path.split(file_path)[1]
            print("%7.1f MB | %8i Bytes | %s" % (
                (uncompressed_size / 1024 / 1024),
                uncompressed_size,
                name,
            ))


class TableData(object):
    def __init__(self):
        super(TableData, self).__init__()
        self._raw_data = []
        self._used_keys = None

    def append(self, **raw_data):
        if self._used_keys is None:
            self._used_keys = raw_data.keys()
        else:
            assert raw_data.keys() == self._used_keys
        self._raw_data.append(raw_data)

    def transform_file_path(self, file_path):
        return {
            "file name": os.path.split(file_path)[1]
        }

    def transform_compressor(self, compressor):
        return {
            "compressor": compressor.get_info()
        }

    def transform_compressed_size(self, compressed_size):
        return {
            "compressed Bytes": "%i Bytes" % compressed_size,
            "compressed MB": "%.1f MB" % (compressed_size / 1024 / 1024),
        }

    def transform_duration(self, duration):
        return {"duration": "%.2f sec." % duration}

    def print_table(self, sort_key, reverse=False):
        assert self._used_keys != None
        assert sort_key in self._used_keys

        # pprint(self._raw_data)

        transformed_data = []
        for raw_data in sorted(self._raw_data, key=lambda x: x[sort_key], reverse=reverse):
            temp = {}
            for key, value in raw_data.items():
                trans_func = getattr(self, "transform_%s" % key, None)
                if trans_func:
                    temp.update(trans_func(value))
                else:
                    temp[key] = value
            transformed_data.append(temp)

        keys = tuple(transformed_data[0].keys())

        table = MarkupTable(head_prefix="", auto_width=True)

        # Hack to format in markdown syntax:
        table.add_tr()
        for key in keys:
            table.add_td(key)

        table.add_tr()
        for key in keys:
            table.add_td("-"*len(key))

        for entry in transformed_data:
            table.add_tr()
            for key in keys:
                table.add_td(entry[key])

        content = table.get_table_markup()
        content = content.strip()
        print(content)



class Benchmark(object):
    def __init__(self, files, out_path, compressors):
        self.files = files
        self.out_path = out_path
        self.compressors = compressors

    def compress_file(self, filepath, compressor):
        out_filename = "%s%s" % (
            os.path.split(filepath)[1],
            compressor.filename_suffix()
        )

        out_filepath = os.path.join(self.out_path, out_filename)
        src_name = os.path.split(filepath)[1]
        sys.stdout.write("| %15s | %14s" % (
            src_name, compressor.get_info()
        ))
        sys.stdout.flush()

        statinfo = os.stat(filepath)
        uncompressed_size = statinfo.st_size

        with open(filepath, "rb") as source_file:
            with open(out_filepath, "wb") as out_file:
                start_time = time.time()
                out_file.write(
                    compressor.compress(source_file.read())
                )

        duration = time.time() - start_time
        statinfo = os.stat(out_filename)
        compressed_size = statinfo.st_size
        percent = (100.0 / uncompressed_size) * compressed_size

        print(" | %6.2fsec | %6.2fMB | %6.2f%% | %s |" %(
            duration, (compressed_size / 1024 / 1024), percent, out_filepath
        ))

        return compressed_size, duration

    def run(self):
        table_data = TableData()

        print("\n\n**run compression:**\n")
        print("| filename | compressor | duration | out size | ratio | out filename |")
        print("| -------- | ---------- | -------- | -------- | ----- | ------------ |")

        for compressor in self.compressors:
            for file_path in self.files:
                compressed_size, duration = self.compress_file(
                    file_path, compressor
                )
                table_data.append(
                    file_path=file_path,
                    compressor=compressor,
                    compressed_size=compressed_size,
                    duration=duration,

                )

        print("\n")
        return table_data


if __name__ == "__main__":
    test_files = (
        "pypyjs-release/lib/pypy.vm.js",
        "pypyjs-release/lib/pypy.vm.js.mem"
    )
    FileInfo(test_files).print_table()

    compressors = []

    # compressors += [Zlib(level) for level in range(0,2)]
    # compressors += [Bzip2(level) for level in range(1,3)]
    # compressors += [Lzma(preset) for preset in range(0,1)]

    compressors += [Zlib(level) for level in range(0,10)]
    compressors += [Bzip2(level) for level in range(1,10)]
    compressors += [Lzma(preset) for preset in range(0,10)]

    for test_file in test_files:
        b = Benchmark([test_file], "./", compressors)
        table_data = b.run()

        print("\n\n**Result sort by duration:**\n")
        table_data.print_table(sort_key="duration")

        print("\n\n**Result sort by compressed size:**\n")
        table_data.print_table(sort_key="compressed_size")

