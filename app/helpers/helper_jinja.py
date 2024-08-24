from datetime import datetime

from datetime import datetime

from datetime import datetime

def month_year_format(date_string):
    try:
        parts = date_string.split()
        if len(parts) == 1:
            # Assume it's just a month number
            month = int(parts[0])
            if 1 <= month <= 12:
                return datetime(2000, month, 1).strftime('%B')
            else:
                return f"Invalid month: {month}"
        elif len(parts) == 2:
            month, year = map(int, parts)
            date_obj = datetime(year=year, month=month, day=1)
            return date_obj.strftime('%B %Y')
        else:
            raise ValueError("Input should be in the format 'month' or 'month year'")
    except Exception as e:
        return f"Error: {str(e)}"

