# rmdups [![Build Status](https://travis-ci.org/jpvlsmv/python-rmdups.svg?branch=master)](https://travis-ci.org/jpvlsmv/python-rmdups)

Remove files from `target_dir` if `reference_dir` has a copy of it already

# Installation

    $ pip install https://github.com/jpvlsmv/python-rmdups.git


# Usage

`rmdups` will scan the --target directory (recursively) and look for files
of an equivalent name under --reference.  If a match is found (and they
have the same sha256 hash), the --target file is removed.

If --refhash is specified, the reference should be a file containing
sha256 hashes as shown by `sha256sum(1)`, or a directory containing a file
`files.sha256sum` with the hash values.  In this operating mode, --target
files will be removed if a match is found for the sha256 hash, regardless
of its path.

To use it:

    $ rmdups --help
    $ rmdups --target /mnt/sdcard --reference /data/pictures
    $ find /data/pictures -type f -exec sha256sum {} + > /tmp/known-files ; \
    > rmdups --target /mnt/sdcard --refhash /tmp/known-files

