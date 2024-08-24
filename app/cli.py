import click
from flask.cli import with_appcontext
from bootstrap.loaddata import load_sample_data

@click.command('load-sample-data')
@with_appcontext
def load_sample_data_command():
    """Load sample data into the database."""
    load_sample_data()
    click.echo('Sample data loaded.')