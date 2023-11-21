import datetime



WWW_1 = "艾滋"
WWW_2 = "hiv"
WWW_3 = "防艾"
WWW_4 = "恐艾"
start_date = "20190101"
end_date = "20231101"
date_format = "%Y%m%d"
start = datetime.datetime.strptime(start_date, date_format)
end = datetime.datetime.strptime(end_date, date_format)

with open('work.txt', 'w',encoding='UTF-8') as f:
    while start < end:
        next_day = start + datetime.timedelta(days=1)
        f.write(f"tweet_by_keyword@{WWW_1}/{start.strftime(date_format)}00/{next_day.strftime(date_format)}00\n")
        f.write(f"tweet_by_keyword@{WWW_2}/{start.strftime(date_format)}00/{next_day.strftime(date_format)}00\n")
        f.write(f"tweet_by_keyword@{WWW_3}/{start.strftime(date_format)}00/{next_day.strftime(date_format)}00\n")
        f.write(f"tweet_by_keyword@{WWW_4}/{start.strftime(date_format)}00/{next_day.strftime(date_format)}00\n")
        start = next_day
