from datetime import datetime

def convert_date(input_date):
    '''
    Returns the area that a specified task is found in using a task_dict.
    
    Keyword Arguments:
    input_date          - The date to convert to a string

    Return Value:
    A string representing the date in the format "MONTH DDth, YYYY".
    '''
    date_object = datetime.strptime(input_date, '%Y%m%d')
    suffix = 'th' if 11 <= int(date_object.day) <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(date_object.day % 10, 'th')
    return date_object.strftime('%B %d{}, %Y').format(suffix)
