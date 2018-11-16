# imgur_upload
for mac os x: adds a workflow service that allows to right click->service->upload to imgur on image files: https://i.imgur.com/k514fLL.png

# requirements

- python 2.7; this should be shipped with all recent mac os x versions
- requests package for python

# installation

First open a terminal and install pip with `sudo easy_install pip` and then install the requests package with `sudo pip install requests`.

Move all files of this repository to `~/Library/Services`. `~/Library/` is hidden by default, you can direct a finder window there with `open ~/Library/Services` in a terminal, or in a finder: in the menu `Go -> Go to folder...`. The folder structure should look like this:

```
    ~/Library/Services/upload to imgur.workflow
    ~/Library/Services/imgur_upload/imgurupload.py
    ~/Library/Services/imgur_upload/imgurauth.py
    ~/Library/Services/imgur_upload/imgur.conf
```

`~/Library/Services/imgur_upload/imgur.conf` will be created by the script after the first authentication with imgur. 
You want to delete this file if you want to re-auth with a different user, or if upload ever stops working since likely the access token has run out (however, this is highly unlikely since right now I'm getting access tokens that last 10 years).

You may have to restart for the service item to show up.

The first time you upload an image the browser will open and ask you to authorize access for this app to your imgur account. On successful authorization a config file is created so that future uploads will start immediately without need for authentication.

contact info for bugs and similar: therealtoastitoasti@gmail.com
