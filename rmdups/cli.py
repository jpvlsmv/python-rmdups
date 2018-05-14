import click
# from pathlib import Path


@click.command()
@click.option('--no-action', '-n', is_flag=True, help='Take no action')
@click.option('--force', '-f', is_flag=True, help='Force removals')
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

    click.echo('Hello world')
    click.echo(sorted(kwargs.items(), key=lambda x: x[0]))
    click.echo(sorted(mytgts))
    # Handling command line behavior:
