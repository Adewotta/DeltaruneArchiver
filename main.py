import bs4 as bs
import requests
import urllib.request
import os, time, json

def downloadDeltarune(KEY,uploadID,name):
    r = requests.get("https://itch.io/api/1/%s/upload/%s/download" % (KEY,uploadID))
    url = json.loads(r.text)['url']
    urllib.request.urlretrieve(url, os.path.abspath("./(%s)%s.zip" % (uploadID,name)))

def checkForUpdates(KEY):
    #Store the upload ID of the games we have already downloaded into this dictioanry
    VersionList = {}
   #Try to open the versionList.txt file, if it doesn't exist or is invalid then 
   #Create a blank versionList.txt file
    try:
        file = open("versionList.txt","r")
        VersionList = json.load(file)
        file.close()
    except:
        VersionList = {}
        file = open("versionList.txt","w")
        file.close()
    
    
    source = requests.get("https://tobyfox.itch.io/deltarune").text
    soup = bs.BeautifulSoup(source, 'html.parser')
    #Download each version

    uploads = soup.find_all(class_="upload")
    for upload in uploads:
        uploadID = upload.find(class_="button download_btn")["data-upload_id"]
        title = upload.find(class_="name")["title"][:-4]
        if uploadID not in VersionList:
            print("New Version Found: (%s)%s" % (uploadID,title))
            #download unarchived vesion of the game
            downloadDeltarune(KEY,uploadID,title)
            #Update Version List
            VersionList[uploadID] = ""
            #Save new version list to file
            versionListJson = json.dumps(VersionList)
            file = open("versionList.txt", "w")
            file.write(versionListJson)
            file.close()
            print("Downloaded: (%s)%s" % (uploadID,title))

if __name__ == "__main__":
    f = open("key.txt","r",encoding = 'utf-8')
    KEY = f.read()
    f.close()
    while 1==1:
        print("Checking for updates...")
        checkForUpdates(KEY)
        print("Finished checking for updates")
        time.sleep(600)