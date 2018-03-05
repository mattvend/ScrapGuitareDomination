# ScrapGuitareDomination
Video and audio files scrapping from www.guitaredomination.com  
**Edit on 3/5/2018**: the site seems to be definitely down  

# Background

I recently decided to learn how to play guitar, and I started online with this website: http://www.guitaredomination.com/
Once the subscription paid, you have access to books that you can download, and to videos stored on a Vimeo private channel that you cannot download.
You are supposed to have unlimited access with your login.

The site went down, and stopped me abruptly in my valiant efforts to learn how to play guitar from Feb. 2016 to May 2016.
Strictly speaking, I can understand that websites can go down, but I expect them to resume shortly, especially when I paid for it. I can easily tolerate 3-4 days of downtime, but it becomes a serious issue to me when it goes down for nothing less than 4 months. 

To mitigate this, I had no choice but to find a way to continue learning guitar when it happens. Doing so means downloading all the videos from the Vimeo private channel. As a solution to my problem, I wrote a Python script to scrap all the audio/video content from the site.

There are 4 learning modules: beginner, lead, blues-1 and blues-2

For each module, my script:
- Creates a directory
- Downloads in the directory all the module related videos
- Downloads in the directory all the module related audio files

My script does not download the books.

# Disclaimer

I am not going to communicate my login/password as my intent is not to give away document you have to pay for. Therefore do not contact me, I will not give you my credentials nor any multimedia files.
My intent is to provide you with a way to get all the multimedia files you need in order to continue learning the guitar, should the website go down one more time. To use the script, you are expected to own a valid login/password to the website.

The script is written in Python3, and should work on Windows/Linux/OSX. It has been used on Windows and OSX.

# Remark

It is also possible to do that manually, but there are in total more than 640 files to download and rename. Better scripting than having to do tedious things.

# Usage
- if not already present, install Python3 on your machine
- Update config.json with your own guitaredomination.com login/password
- then, in a shell, type: python scrap.py

