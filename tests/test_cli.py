import pytest
from click.testing import CliRunner
from rmdups import cli
from pathlib import Path


@pytest.fixture
def runner():
    return CliRunner()


files = [
            (Path('target'), 'file1.txt', b'Hello World\n',
                b'e59ff97941044f85df5297e1c302d260',
                b'd2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26'),
            (Path('target'), 'file2.txt', b'Duplicate detected\n',
                b'4d826e209ebe9ac1592265c4e4367515',
                b'73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc'),
            (Path('target'), 'file3.txt', b'Duplicate detected\n',
                b'4d826e209ebe9ac1592265c4e4367515',
                b'73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc'),
            (Path('reference'), 'file2.txt', b'Duplicate detected\n',
                b'4d826e209ebe9ac1592265c4e4367515',
                b'73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc'),
            (Path('reference'), 'files.md5sum', b'4d826e209ebe9ac1592265c4e4367515  file2.txt\n',
                None, None),
            (Path('reference'), 'files.sha256sum',
                b'73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc  file2.txt\n',
                None, None),
        ]


def mk_files():
    for (p, nm, content, md5, sha) in files:
        r = Path(p)
        if not r.is_dir():
            r.mkdir()
        with open(r / nm, 'wb') as f:
            f.write(content)


def test_reference(runner):
    with runner.isolated_filesystem():
        mk_files()

        result = runner.invoke(cli.cli,
                               ["-r", "reference", "--debug", "all", "target"])
        assert not result.exception
        assert ''.join(result.output.split()).replace('\\', '/') == ''.join(r'''
Operating on reference file reference/files.sha256sum
Read 1 hashes
Working with target directory target
target/file1.txt
d2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26 is new
target/file2.txt
73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc seen before
target/file3.txt
73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc seen before
            '''.split())


def test_reference_dir_auto_from_hash(runner):
    with runner.isolated_filesystem():
        mk_files()
        result = runner.invoke(cli.cli,
                               ["-h", "md5", "-t", "target",
                                "-r", "reference", "--debug", "all"])
        assert not result.exception
        assert ''.join(result.output.split()) == ''.join(r'''
Operating on reference file reference\files.md5sum
Read 1 hashes
Working with target directory target
target\file1.txt
e59ff97941044f85df5297e1c302d260 is new
target\file2.txt
4d826e209ebe9ac1592265c4e4367515 seen before
target\file3.txt
4d826e209ebe9ac1592265c4e4367515 seen before
            '''.split())


def test_hash_mismatch(runner):
    with runner.isolated_filesystem():
        mk_files()
        result = runner.invoke(cli.cli,
                               ["-R", "reference/files.md5sum", "--debug", "all", "target"])
        assert not result.exception
        assert ''.join(result.output.split()) == ''.join(r'''
Read 1 hashes
Working with target directory target
target\file1.txt
d2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26 is new
target\file2.txt
73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc is new
target\file3.txt
73b3a8cbcde30600ac05a6d19d7ca4569b8bad67fd0d494eb53ff504312d20bc is new
'''.split())
