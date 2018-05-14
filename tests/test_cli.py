import pytest
from click.testing import CliRunner
from rmdups import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.cli,
                           ["-n", "-f", "-h", "foo", "-t", ".", "-t", "/",
                            "-r", "..", "/", "/users", '--debug=cli'])
    assert not result.exception
    assert result.output == r'''
    Hello world,
    [('debug', 'cli'), ('force', True), ('hash_type', 'foo'), \
            ('no_action', True), ('reference', '..'), ('reference_file', \
            None), ('target', ('.', '/')), ('targets', ('/', '/users'))]
    ['.', '/', '/', '/users']
    '''
