import time
t = time.localtime()#tells local time in seconds(on which device this program is bein executing)
formatted_time = time.strftime("%Y-%m-%d %H:%H:%S", t)


print(formatted_time)