import requests
import csv
from rich.panel import Panel as panel
from rich import print as prints

M2 = "[#FF0000]"  # MERAH
H2 = "[#00FF00]"  # HIJAU
K2 = "[#FFFF00]"  # KUNING
B2 = "[#00C8FF]"  # BIRU
P2 = "[#FFFFFF]"  # PUTIH

def get_all_shopee_reviews(url, batch_size=50):
    all_reviews = []
    offset = 0

    while True:
        current_url = f"{url}&limit={batch_size}&offset={offset}"
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            data = response.json()
            reviews = data.get('data', {}).get('ratings', [])
            if not reviews:
                break
            all_reviews.extend(reviews)
            offset += batch_size
            print(f"[%] Mengambil ulasan dari Shopee {offset} ...", end='\r')
        except requests.exceptions.RequestException as e:
            print("\nGagal mengambil data:", e)
            return []
    
    print("\nUlasan telah selesai diambil.")
    return all_reviews

def save_reviews_to_csv(all_reviews, filename='shopee_reviews.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nama', 'Rating', 'Ulasan']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, review in enumerate(all_reviews[:250], start=1):
            star_rating = int(review.get('rating_star', 0))
            bintang = "★" * star_rating + "☆" * (5 - star_rating)
            comment = review.get('comment', '').strip()
            if not comment:
                comment = "Pelanggan tidak memberikan ulasan"
            writer.writerow({'Nama': review.get('author_username', 'Unknown'),
                             'Rating': bintang,
                             'Ulasan': comment})

def main():
    url = "https://shopee.co.id/api/v2/item/get_ratings?exclude_filter=1&filter=0&filter_size=0&flag=1&fold_filter=0&itemid=23961394289&relevant_reviews=false&request_source=2&shopid=202450576&tag_filter=&type=0&variation_filters="
    all_reviews = get_all_shopee_reviews(url)
    if all_reviews:
        print("Daftar 50 Ulasan Pertama:")
        for i, review in enumerate(all_reviews[:250], start=1):
            star_rating = int(review.get('rating_star', 0))
            bintang = "★" * star_rating + "☆" * (5 - star_rating)
            comment = review.get('comment', '').strip()
            if not comment:
                comment = "Pelanggan tidak memberikan ulasan"
            prints(panel(f"[green]{P2}Nama: {H2}{review.get('author_username', 'Unknown')}\n{P2}Rating: {K2}{bintang}\n{P2}Ulasan: {H2}{comment}[/]", title=f"[[green]{i}[/]]", style=f"bold white"))
            print()

        save_reviews_to_csv(all_reviews)
        print("[OK] Data ulasan telah disimpan ke dalam file 'shopee_reviews.csv'")
    else:
        print("Tidak ada ulasan yang ditemukan.")

if __name__ == "__main__":
    main()
