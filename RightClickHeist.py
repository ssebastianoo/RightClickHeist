import requests, time, sys

webhook_url = None
if len(sys.argv) > 1:
    webhook_url = sys.argv[1]

offset = 0

while True:
    url = f"https://api.opensea.io/api/v1/assets?order_direction=desc&offset={offset}&limit=1"
    response = requests.request("GET", url)
    responselist = response.text.split(",")
    for item in responselist:
        if '"image_url"' in item and "null" not in item:
            item = item.split('":"')
            if len(item[1]) > 5:
                url = item[1][:-1]
                urlparts = url.split("/")
                name = urlparts[-1]
                print(url)
                image = requests.get(url)
                if webhook_url:
                    requests.post(webhook_url, files={"file": ('nft.png', image.content)})
                else:
                    if "." not in name:
                        with open(name + ".png", "wb") as myfile:
                            myfile.write(image.content)
                    else:
                        with open(name, "wb") as myfile:
                            myfile.write(image.content)
            break
    offset += 1
    time.sleep(.25)
