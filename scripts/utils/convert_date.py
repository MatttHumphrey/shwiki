from datetime import datetime

def convert_date(input_date):
    date_object = datetime.strptime(input_date, '%Y%m%d')
    suffix = 'th' if 11 <= int(date_object.day) <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(date_object.day % 10, 'th')
    return date_object.strftime('%B %d{}, %Y').format(suffix)