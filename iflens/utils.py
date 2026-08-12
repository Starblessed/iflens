from datetime import datetime

def time_signed_print(*args, **kwargs):
    stamp = f'[{datetime.now().strftime("%Y/%m/%d - %H:%M:%S")}]'
    
    print(stamp, *args, **kwargs)
    