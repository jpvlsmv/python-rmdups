import pytest
from click.testing import CliRunner
from rmdups import cli
from pathlib import Path


@pytest.fixture
def runner():
    return CliRunner()


def test_reference_detection_byhash(runner):
    with runner.isolated_filesystem():
        mk_files()
        result = runner.invoke(cli.cli,
                               ["-h", "md5", "-t", "target",
                                "-r", "reference"])
        assert not result.exception
        assert ''.join(result.output.split()) == ''.join(r'''
Operating on reference file reference/files.md5sum
Read 1 hashes
Working with target directory target
target/file1.txt
target/file2.txt
4d034101596def954ebccf4e7275cb43 seen before
target/file3.txt
4d034101596def954ebccf4e7275cb43 seen before
            '''.split())


def mk_files():
    r = Path('reference')
    r.mkdir()
    with open(r / "file2.txt", 'wb') as f:
        f.write(b'Duplicate detected\n')
    with open(r / "files.md5sum", 'wb') as f:
        f.write(b'4d034101596def954ebccf4e7275cb43  file2.txt\n')
    with open(r / "files.sha256sum", 'wb') as f:
        f.write(
                b'5207f1a1f5390a25358aa34969e2aeb275180bce7c62db8c4c64237dee722f52  file2.txt\n'
                b'df24ef8c58e9754070346a01d6aefe6792f1e800d2dbc74dface6ecb93f537f9  files.md5sum\n'
                )
    t = Path('target')
    t.mkdir()
    with open(t / "file1.txt", 'wb') as f:
        f.write(b'Hello World\n')
    with open(t / "file2.txt", 'wb') as f:
        f.write(b'Duplicate detected\n')
    with open(t / "file3.txt", 'wb') as f:
        f.write(b'Duplicate detected\n')


def test_reference(runner):
    with runner.isolated_filesystem():
        mk_files()

        result = runner.invoke(cli.cli,
                               ["-r", "reference", "target"])
        assert not result.exception
        assert ''.join(result.output.split()) == ''.join(r'''
Operating on reference file reference/files.sha256sum
Read 2 hashes
Working with target directory target
target/file1.txt
target/file2.txt
target/file3.txt
            '''.split())


def test_hash_mismatch(runner):
    with runner.isolated_filesystem():
        mk_files()
        result = runner.invoke(cli.cli,
                               ["-R", "reference/files.md5sum", "target"])
        assert not result.exception
        assert ''.join(result.output.split()) == ''.join(r'''
Operating on reference file reference/files.md5sum
Read 1 hashes
Working with target directory target
target/file1.txt
target/file2.txt
target/file3.txt
            '''.split())
