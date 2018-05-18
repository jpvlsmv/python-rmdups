import pytest
from click.testing import CliRunner
from rmdups import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.cli,
                           ['--debug=cli',
                            "-n", "-f", "-h", "md5", "-t", ".", "-t", "/",
                            "-r", "..", "/", "/users"])
    assert ''.join(result.output.split()) == ''.join(r'''
    Hello world,
    [('debug', 'cli'), ('force', True), ('hash_type', 'md5'),
     ('no_action', True), ('reference', '..'), ('reference_file', None),
     ('target', ('.', '/')), ('targets', ('/', '/users'))]
    ['.', '/', '/', '/users']
    '''.split())


def test_reference_detection_byhash(runner):
    result = runner.invoke(cli.cli,
                           ["-h", "md5", "-t", "samples/target",
                            "-r", "samples/reference"])
    assert not result.exception
    assert ''.join(result.output.split()) == ''.join(r'''
Operating on reference file samples\reference\files.md5sum
Read 1 hashes
Working with target directory samples\target
samples\target\file1.txt
samples\target\file2.txt
45a7b49cfdc7b16d03ed544dfa4d8922 seen before
samples\target\file3.txt
45a7b49cfdc7b16d03ed544dfa4d8922 seen before
        '''.split())


def test_reference(runner):
    result = runner.invoke(cli.cli,
                           ["-r", "samples/reference", "samples/target"])
    assert not result.exception
    assert ''.join(result.output.split()) == ''.join(r'''
Operating on reference file samples\reference\files.sha256sum
Read 2 hashes
Working with target directory samples\target
samples\target\file1.txt
samples\target\file2.txt
5207f1a1f5390a25358aa34969e2aeb275180bce7c62db8c4c64237dee722f52 seen before
samples\target\file3.txt
5207f1a1f5390a25358aa34969e2aeb275180bce7c62db8c4c64237dee722f52 seen before
        '''.split())


def test_hash_mismatch(runner):
    result = runner.invoke(cli.cli,
                           ["-R", "samples/reference/files.md5sum", "samples/target"])
    assert not result.exception
    assert ''.join(result.output.split()) == ''.join(r'''
Operating on reference file samples\reference\files.md5sum
Read 1 hashes
Working with target directory samples\target
samples\target\file1.txt
samples\target\file2.txt
samples\target\file3.txt
        '''.split())
