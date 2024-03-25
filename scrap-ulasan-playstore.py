import csv
from google_play_scraper import app, reviews_all

app_package = 'com.facebook.katana' # Ganti Ini Aja
info = app(app_package)
csv_file = open('reviews.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Rating', 'Oleh', 'Ulasan'])

result = reviews_all(
    app_package,
    lang='id',
    sleep_milliseconds=1000,
    filter_score_with=None
)

for review in result:
    rating = '*' * review['score']
    csv_writer.writerow([rating, review['userName'], review['content']])
    print(f"Rating: {rating}")
    print(f"Oleh: {review['userName']}")
    print(f"Ulasan: {review['content']}")
    print()

print("-"*20)
print("Developed by @tian")
print(f"Nama Aplikasi: {info['title']}")
print(f"Jumlah Unduhan: {info['installs']}")
print(f"Peringkat: {info['score']}")
csv_file.close()