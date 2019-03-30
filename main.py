import time
import urllib.request
import lxml.html

host = "https://undraw.co"
page = "/illustrations/load/0"

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

        file = open('./images/' + svgName + '.svg', 'w')
        file.write(svgResponse.decode('utf-8'))
        file.close()

        print("Downloaded", svgName)

        time.sleep(0.5)

    page = tree.xpath('//a[@href]')[-1].attrib['href']
