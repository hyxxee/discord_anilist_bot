import requests
from PIL import Image
from io import BytesIO
from collections import Counter

ANILIST_API_URL = 'https://graphql.anilist.co/'

def get_dominant_color(image_url):
    """Mengambil warna dominan dari gambar."""
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((img.width // 10, img.height // 10))  # Mengurangi ukuran gambar untuk mempercepat proses
    img = img.convert("RGB")

    # Mengambil semua pixel
    pixels = list(img.getdata())
    # Menghitung frekuensi setiap warna
    most_common = Counter(pixels).most_common(1)

    return most_common[0][0]  # Mengembalikan warna dominan

def rgb_to_int(rgb):
    """Konversi tuple RGB ke integer HEX."""
    return (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]

def fetch_anime_data(title):
    query = """
    query ($title: String) {
        Media (search: $title, type: ANIME) {
            title {
                romaji
            }
            description
            type
            episodes
            startDate {
                day
                month
                year
            }
            endDate {
                day
                month
                year
            }
            status
            genres
            averageScore
            rankings {
                rank
            }
            coverImage {
                large
            }
        }
    }
    """
    variables = {'title': title}
    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()
        media = data['data']['Media']
        cover_image_url = media['coverImage']['large']
        dominant_color = get_dominant_color(cover_image_url)
        return {
            'title': media['title'],
            'description': media['description'],
            'type': media['type'],
            'episodes': media['episodes'],
            'startDate': media['startDate'],
            'endDate': media['endDate'],
            'status': media['status'],
            'genres': media['genres'],
            'averageScore': media['averageScore'],
            'rankings': media['rankings'],
            'coverImage': media['coverImage'],
            'dominantColor': dominant_color
        }
    else:
        return None

def fetch_manga_data(title):
    query = """
    query ($title: String) {
        Media (search: $title, type: MANGA) {
            title {
                romaji
            }
            description
            type
            chapters
            startDate {
                day
                month
                year
            }
            endDate {
                day
                month
                year
            }
            status
            genres
            averageScore
            rankings {
                rank
            }
            coverImage {
                large
            }
        }
    }
    """
    variables = {'title': title}
    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()
        media = data['data']['Media']
        cover_image_url = media['coverImage']['large']
        dominant_color = get_dominant_color(cover_image_url)
        return {
            'title': media['title'],
            'description': media['description'],
            'type': media['type'],
            'chapters': media['chapters'],
            'startDate': media['startDate'],
            'endDate': media['endDate'],
            'status': media['status'],
            'genres': media['genres'],
            'averageScore': media['averageScore'],
            'rankings': media['rankings'],
            'coverImage': media['coverImage'],
            'dominantColor': dominant_color
        }
    else:
        return None

def format_date(date):
    if date['day'] and date['month'] and date['year']:
        return f"{date['day']:02d}/{date['month']:02d}/{date['year']}"
    return "?"
