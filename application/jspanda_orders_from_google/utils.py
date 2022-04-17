from datetime import datetime
import click

def validate_date(ctx,param,value):
    try:
        if isinstance(value, str):
            datetime.strptime(value, "%Y%m%d")
            return value        
    except ValueError:
        raise click.BadParameter("Date must be in format YYYYMMDD.")
