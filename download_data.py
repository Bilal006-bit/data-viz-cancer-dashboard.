import urllib.request
import os

data_dir = r"c:\Users\Bilal\Desktop\UE\Data Visualization\final-project-cancer-dashboard\data"

urls = {
    "death-rate-from-cancer.csv": "https://ourworldindata.org/grapher/death-rate-from-cancer.csv?v=1&csvType=full&useColumnShortNames=false",
    "total-cancer-deaths-by-type.csv": "https://ourworldindata.org/grapher/total-cancer-deaths-by-type.csv?v=1&csvType=full&useColumnShortNames=false"
}

for filename, url in urls.items():
    print(f"Downloading {filename}...")
    filepath = os.path.join(data_dir, filename)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("Done!")
