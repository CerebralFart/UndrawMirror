import datetime
import os
import time
import urllib.request
import lxml.html

folder = './images/'
host = "https://undraw.co"
page = "/illustrations/load/0"

# Remove all pre-existing images
if os.path.isdir(folder):
    print("Cleaning images folder")
    for file in os.listdir(folder):
        os.remove(folder + file)
else:
    os.mkdir(folder)

while page is not None:
    request = urllib.request.Request(host + page)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0')
    response = urllib.request.urlopen(request).read()

    print("Loaded page", page)

    tree = lxml.html.fromstring(response)

    images = tree.xpath('//div[@class="item"]')

    for image in images:
        svgPath = image.xpath('a[@data-src]')[0].attrib['data-src']
        svgName = image.xpath('h4/text()')[0]

        svgRequest = urllib.request.Request(svgPath)
        svgRequest.add_header('User-Agent',
                              'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0')
        svgResponse = urllib.request.urlopen(svgRequest).read()

        fname = folder + svgName + '.svg'

        file = open(fname, 'w')
        file.write(svgResponse.decode('utf-8'))
        file.close()

        print("Downloaded", svgName)
        os.system("git add \"%s\"" % fname)

        time.sleep(0.5)

    aList = tree.xpath('//a[@href]')
    if len(aList) == 0:
        page = None
    else:
        page = aList[-1].attrib['href']

date = datetime.datetime.now().strftime("%d/%m/%y")
os.system("git commit -m \"Images %s\"" % date)
