from conans import CMake, ConanFile, tools
import os

# https://github.com/giorgioazzinnaro/rocksdb/blob/master/INSTALL.md

class RocksdbConan(ConanFile):
    name = "RocksDB"
    version = "5.17.2"
    license = "https://github.com/facebook/rocksdb/blob/master/COPYING"
    url = "https://github.com/ambroff/conan-RocksDB"
    description = "A library that provides an embeddable, persistent key-value store for fast storage."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    source_tgz = "https://github.com/facebook/rocksdb/archive/v%s.tar.gz" % version
    checksum = '101f05858650a810c90e4872338222a1a3bf3b24de7b7d74466814e6a95c2d28'

    requires = (
        "zlib/1.2.11@conan/stable",
        "bzip2/1.0.6@conan/stable",
        "lz4/1.8.3@bincrafters/stable",
        "snappy/1.1.7@bincrafters/stable",
        "zstd/1.3.5@bincrafters/stable",
        "glog/0.3.5@bincrafters/stable",
    )

    def source(self):
        self.output.info("Downloading %s" %self.source_tgz)
        tools.get(self.source_tgz, sha256=self.checksum)

    @property
    def subfolder(self):
        return "rocksdb-%s" % self.version

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(
            source_folder='rocksdb-{}'.format(self.version),
            defs={
                'CMAKE_POSITION_INDEPENDENT_CODE': True,
                'WITH_GFLAGS': False,
                'WITH_TESTS': False,

                # FIXME: Need to patch find_package() usage to find these appropriately?
                'WITH_LZ4': False,
                'WITH_ZLIB': False,
                'WITH_ZSTD': False,
                'WITH_SNAPPY': False,
            })
        return cmake
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.Apache", src=self.subfolder, keep_path=False)
        self.copy("LICENSE.leveldb", src=self.subfolder, keep_path=False)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["rocksdb"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
