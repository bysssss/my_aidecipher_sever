from time import time
from datetime import datetime, timedelta, timezone
from decimal import Decimal


def timestamp_unix():
    return int(round(time(), 3)*1000)


def timestamp():
    return round(time(), 3)


def decimal():
    return round(Decimal(time()), 3)


def date(delta=9, fmt=None):  # '%Y-%m-%d %H:%M:%S'
    td = timedelta()
    if isinstance(delta, int):
        td = timedelta(hours=int(delta))

    now = datetime.utcnow() + td
    if fmt is not None:
        now = datetime.strptime(now.strftime(fmt), fmt)
    return now
    # return now.strftime('%Y-%m-%d %H:%M:%S')
    # return now.strftime(f.encode('unicode-escape').decode()).encode().decode('unicode-escape')


def ts_from_dt(_dt):
    _ts = datetime.timestamp(_dt)
    return _ts


def dt_from_ts(_ts, delta=9):
    tz = timezone.utc
    if isinstance(delta, int):
        tz = timezone(timedelta(hours=int(delta)))
    _dt = datetime.fromtimestamp(_ts, tz=tz)
    return _dt


def decimal_from_iso(_iso):
    try:
        _decimal = Decimal(datetime.timestamp(datetime.fromisoformat(_iso)))
    except Exception:
        return None
    return _decimal
