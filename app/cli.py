import click
from flask.cli import with_appcontext
from bootstrap.loaddata import dummy_pmsperf, load_sample_data,load_pms_data,create_schema,populate_pms_nav,load_amc_users,populate_category_master

@click.command('load-sample-data')
@with_appcontext
def load_sample_data_command():
    print(" load_sample_data_command()")
    
    # print('creating schema')
    # create_schema()

    # click.echo('Schema Created.')
    
    # """Load sample data into the database."""
    # load_sample_data()
    # click.echo('Sample data loaded.')
    
    # load_pms_data()
    # click.echo('PMS data loaded.')
    
    # dummy_pmsperf()
    # click.echo('PMS Performance Dummy data loaded for July 2024.')

    # populate_category_master()
    # click.echo('populate_category_master loaded.')
    
    # loadPmsSectors()
    
    