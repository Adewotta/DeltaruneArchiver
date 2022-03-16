import bs4 as bs
import requests
import urllib.request
import os, time, json

def downloadDeltarune(KEY,uploadID,name):
    try:
        r = requests.get("https://itch.io/api/1/%s/upload/%s/download" % (KEY,uploadID))
        url = json.loads(r.text)['url']
        urllib.request.urlretrieve(url, os.path.abspath("./(%s)%s.zip" % (uploadID,name)))
        return True
    except:
        return False

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
    
    try:
        source = requests.get("https://tobyfox.itch.io/deltarune")
        if source.status_code != 200:
            print("Error: Bad Status Code")
            return False
    except:
        print("Error connecting to https://tobyfox.itch.io/deltarune")
        return False
        
    soup = bs.BeautifulSoup(source.text, 'html.parser')
    #Download each version

    uploads = soup.find_all(class_="upload")
    for upload in uploads:
        uploadID = upload.find(class_="button download_btn")["data-upload_id"]
        title = upload.find(class_="name")["title"][:-4]
        if uploadID not in VersionList:
            print("New Version Found: (%s)%s" % (uploadID,title))
            #download unarchived vesion of the game
            if downloadDeltarune(KEY,uploadID,title):
                #Update Version List
                VersionList[uploadID] = ""
                #Save new version list to file
                versionListJson = json.dumps(VersionList)
                file = open("versionList.txt", "w")
                file.write(versionListJson)
                file.close()
                print("Downloaded: (%s)%s" % (uploadID,title))
            else:
                print("Please check API key ")
    return True

if __name__ == "__main__":

#Check for file privilages
    try:
        f = open("key.txt","w+")
        f.close()
    except:
        print("Could not open file, permission denied")
        exit(1)

    #Get users API key
    f = open("key.txt","r",encoding = 'utf-8')
    KEY = f.read()
    f.close()

    while 1==1:
        print("Checking for updates...")
        if checkForUpdates(KEY):

            print("Finished checking for updates")
        else:
            print("Error checking for updates")
        time.sleep(600)