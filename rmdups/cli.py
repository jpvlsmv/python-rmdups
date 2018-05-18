import click
from pathlib import Path
from collections import defaultdict
import re
import hashlib


@click.command()
@click.option('--no-action', '-n', is_flag=True, default=False, help='Take no action')
@click.option('--force', '-f', is_flag=True, default=False, help='Force removals')
@click.option('--debug', nargs=1, help='')
@click.option('--hash-type', '-h', nargs=1, required=False,
              help='Hash function to use', default='sha256')
@click.option('--target', '-t', nargs=1, required=False,
              multiple=True,
              type=click.Path(exists=True, file_okay=False),
              help='Directory to scan/remove from')
@click.option('--reference', '-r', nargs=1, required=False,
              type=click.Path(exists=True, file_okay=False),
              help='Directory that has the original files')
@click.option('--reference-file', '-R', nargs=1, required=False,
              type=click.Path(exists=True, dir_okay=False),
              help='File list of hashes')
@click.argument('targets', required=False, nargs=-1,
                type=click.Path(exists=True, file_okay=False))
def cli(**kwargs):
    """Remove files from target_dir if reference_dir has a copy"""
    mytgts = list(kwargs['targets']) + (list(kwargs['target']))

    if 'debug' in kwargs and kwargs['debug'] == 'cli':
        click.echo('Hello world,')
        click.echo(sorted(kwargs.items(), key=lambda x: x[0]))
        click.echo(sorted(mytgts))
        exit(0)

    if kwargs['hash_type'] not in hashlib.algorithms_available:
        click.echo(f'Unknown hash type {kwargs["hash_type"]}')
        exit(3)

    # Find a reference path or file
    if 'reference_file' in kwargs and kwargs['reference_file'] is not None:
        myref = Path(kwargs['reference_file'])
    elif 'reference' in kwargs:
        myref = Path(kwargs['reference']) / Path(f'files.{kwargs["hash_type"]}sum')
        if not myref.is_file():
            click.echo(f'Problem with reference file {myref}')
            exit(3)

    click.echo(f'Operating on reference file {myref}')

    linepattern = re.compile('(?P<hash>\w+) [ *](?P<path>.*)')
    reference = defaultdict(list)
    with myref.open() as f:
        for line in f:
            (h, p) = linepattern.match(line).groups()
            reference[h.lower()].append(p)

    click.echo(f'Read {len(reference)} hashes')

    for t in [Path(_) for _ in mytgts]:
        click.echo(f'Working with target directory {t}')
        for tpath in t.rglob('*.*'):
            click.echo(tpath)
            h = hashlib.new(kwargs['hash_type'], data=tpath.read_bytes())

            if h.hexdigest().lower() in reference:
                click.echo(f'{h.hexdigest()} seen before')
                if kwargs['force']:
                    click.echo('\tREMOVED!!!')
                    tpath.unlink()
