# GroupMeBackup

This is a simple Python script to backup your GroupMe chats. The only requirement is that you have a GroupMe dev account (and as such, an [Access Token](## Access-Token)).

## Running

Running should be relatively straightforward:
```
python GroupMeBackup.py
```
This will first prompt the user for their access token. Upon entering the access token, the user is shown 15 of their groups. 
Entering the index of the group they want to backup will select that group ID, otherwise the user can move to the next or previous pages of their chats to select another chat. 

```
Enter Access Token: MY-SUPER-SECRET-ACCESS-TOKEN
[0] Ya bois
[1] Secret Meeting
[2] Illuminati
[3] ???
[4] Yeet
[5] Math Class
[6] School Project
[7] Work 
[8] Memes
[9] This is just bots
[10] Group Of Friends That Are Entirely Coincidental
[11] Study Group
[12] Crew
[13] Mysterious Things
[14] Book Club 📖
Which group would you like to backup? (# or 'next/prev'): 
```

Once you press enter, the script will pull all your messages from that group. 
You then have a couple printing options. Make sure to enter them with a space inbetween, or just 'e' for all. 

```
Options:
    (u)sername: prints usernames before message
    (t)ime: prints the absolute time out
    (f)avorites: prints out number of favorites on message
    (a)ttachments: saves all attachments to folder
    (e)verything: all options true
Choose any options you want (i.e. 'u t'): 
```

Note that (a) will create an Attachments folder and download all the gallery images from the groupchat. This may take some time for larger groups.

Then voila! You should have a backup text file along with chronological attachments (if you so choose) saved. 

## Access Token
