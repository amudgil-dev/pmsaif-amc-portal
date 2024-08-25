import click
from flask.cli import with_appcontext
from bootstrap.loaddata import load_sample_data,load_pms_data,create_schema,populate_pms_nav

@click.command('load-sample-data')
@with_appcontext
def load_sample_data_command():
    
    create_schema()
    click.echo('Schema Created.')
    
    # """Load sample data into the database."""
    # load_sample_data()
    click.echo('Sample data loaded.')
    
    load_pms_data()
    click.echo('PMS data loaded.')
    
    # populate_pms_nav()
    
    