from datetime import UTC, datetime


def time_signed_print(*args, **kwargs):
    stamp = f"[{datetime.now(tz=UTC).strftime('%Y/%m/%d - %H:%M:%S')}]"

    print(stamp, *args, **kwargs)
