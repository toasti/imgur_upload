# uploads the image file passed in the argument to imgur
# requires the requests package. install pip with "sudo easy_install pip" and then "sudo pip install requests"

import requests
import base64
import webbrowser
import sys, os.path
import imgurauth

client_id="3bb4ea8e2954a26"
access_token=""
refresh_token=""
conf_file = "imgur.conf"

if len(sys.argv) != 2:
    print("error: pass an image as argument")
    sys.exit()

path=sys.argv[1]

print("### retrieving access token")

if os.path.isfile(conf_file):
    # we have an existing config file, read tokens
    with open(conf_file, "r") as r:
        line1 = r.readline()
        line2 = r.readline()
        access_token = line1.split("access_token=")[1]
        access_token = access_token.split("\n")[0]
        refresh_token = line2.split("refresh_token=")[1]
        refresh_token = refresh_token.split("\n")[0]
        r.close()
else:
    # no config file, request user to oauth
    imgurAuth = imgurauth.TokenHandler("3bb4ea8e2954a26")
    (access_token,refresh_token) = imgurAuth.get_access_token()
    with open(conf_file, "w") as w:
        w.write("access_token="+access_token+"\n")
        w.write("refresh_token="+refresh_token+"\n")
    w.close()

print("### encoding to base64")

with open(path, 'rb') as fd:
    contents = fd.read()
    b64 = base64.b64encode(contents)

apiurl = "https://api.imgur.com/3/image"

data = {
            'image': b64,
            'type': 'base64',
        }

headers = {'Authorization': 'Bearer '+access_token}

print("### uploading")

response = requests.request("POST", apiurl, data=data, headers=headers)
response = response.json()


if response['success']:
    print("### SUCCESS")
    new = 2
    imageurl=response['data']['link']
    imageurl.replace("\\","")
    webbrowser.open(imageurl,new=new)
    sys.exit(0)
else:
    print("### OOPS! something went wrong during the upload")
    print(response.text)
    sys.exit(1)