from datetime import datetime, date

def date_from_ldap_timestamp(timestamp):
    """ Takes an LDAP date (In the form YYYYmmdd
        with whatever is after that) and returns a
        datetime.date object.
    """
    # only check the first 8 characters: YYYYmmdd
    numberOfCharacters = len("YYYYmmdd")
    timestamp = timestamp[:numberOfCharacters]
    try:
        day = datetime.strptime(timestamp, '%Y%m%d')
        return date(year=day.year, month=day.month, day=day.day)
    except:
        return None
