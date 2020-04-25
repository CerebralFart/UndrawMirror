import datetime
import os
import json
import time
import urllib.request


def get_page(page):
    request = urllib.request.Request(page)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0')
    return urllib.request.urlopen(request).read()


folder = './images/'

# Remove all pre-existing images
if os.path.isdir(folder):
    print("Cleaning images folder")
    for file in os.listdir(folder):
        os.remove(folder + file)
else:
    os.mkdir(folder)

hasMore = True
page = 0
images = []

while hasMore:
    print("Loading page", page)
    response = get_page("https://undraw.co/api/illustrations?page=" + str(page))

    data = json.loads(response.decode('utf-8'))
    hasMore = data['hasMore']
    page = data['nextPage']

    for illustration in data['illustrations']:
        images.append((
            illustration['title'],
            illustration['image']
        ))

print("Loaded all pages")

for i in range(len(images)):
    name, location = images[i]
    image = get_page(location)

    fname = folder + name + '.svg'
    file = open(fname, 'w')
    file.write(image.decode('utf-8'))
    file.close()

    print("[%04d/%04d] Downloaded %s" % (i + 1, len(images), name))

    os.system("git add \"%s\"" % fname)
    time.sleep(0.5)

date = datetime.datetime.now().strftime("%d/%m/%y")
os.system("git commit -m \"Images %s\"" % date)
