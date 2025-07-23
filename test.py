from bs4 import BeautifulSoup
from datetime import datetime, timedelta

n_input = input("読み取る動画数は？（空で全件）: ")
N = int(n_input) if n_input.strip() else None 
D = 0.7 #視聴時間
path = 'watch-history.html'
#path = 'watch-history.html'

with open(path, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

entries = soup.find_all("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")

watch_data = [] 

for i, entry in enumerate(entries):
    a_tags = entry.find_all("a")
    #print(a_tags)
    if a_tags:
        title = a_tags[0].text.strip()
    else:
        title = "(タイトルなし)"

    lines = list(entry.stripped_strings)
    if lines:
        watched_time = lines[-1]
    else:
        watched_time = "(日時不明)"

    time_str1 = watched_time.replace(" JST", "")
    fmt = "%Y/%m/%d %H:%M:%S"
    try:
        dt1 = datetime.strptime(time_str1, fmt)
    except ValueError:
        continue

    watch_data.append([title, dt1])

    if N is not None and i == N:
        break

total_duration = timedelta(0)

for i in range(len(watch_data) - 1):
    curwatch = watch_data[i][1]
    nextwatch = watch_data[i + 1][1]
    delta = curwatch - nextwatch
    if delta <= timedelta(hours=D) and delta > timedelta(0):
        total_duration += delta

if len(watch_data) >= 2:
    print(f"{watch_data[-1][1]}から{watch_data[1][1]}の視聴時間を推定します。")
else:
    print("視聴日時が十分にありません。")

print(f"総再生時間 (動画数:{N} ): {total_duration}")

last = int(input("視聴履歴を表示する？(0: No , 1: Yes)"))
if last == 1:
    print("\n--- 視聴履歴一覧 ---")
    for title, dt in watch_data:
        print(f"{dt} - {title}")


print("end!")
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 月ごとの視聴時間を格納
monthly_duration = defaultdict(timedelta)

for i in range(len(watch_data) - 1):
    curwatch = watch_data[i][1]
    nextwatch = watch_data[i + 1][1]
    delta = curwatch - nextwatch
    if timedelta(0) < delta <= timedelta(hours=D):
        month = curwatch.strftime("%Y-%m")  # 例: "2025-07"
        monthly_duration[month] += delta

# 月ごとのデータをソート
months = sorted(monthly_duration.keys())
durations = [monthly_duration[month].total_seconds() / 3600 for month in months]  # 時間に変換

# グラフ描画
plt.figure(figsize=(10, 6))
plt.bar(months, durations, color='mediumseagreen', edgecolor='black')
plt.xticks(rotation=45)
plt.xlabel("Year-Month")
plt.ylabel("WatchTime (h)")
plt.title("WatchTime Per Month")
plt.tight_layout()
plt.grid(axis='y')
plt.show()
