#Bouncy Castle

## Install
	git clone git://github.com/C4ptainCrunch/bouncycastle.git
	virtualenv --distribute --no-site-packages ve 
	source ve/bin/activate
	pip install -r requirements.txt
	
### Config
TODO

(check `config.py` for an example and put the values you want to overwrite in `production.py`)

### Run
You should run `web.py` for the web interface and `convert.py` to convert the videos.

### Dependencies
Bouncy castle uses `python2.7+` and `youyube-dl` witch uses `ffmpeg`

##Bugs/To do:

* Url like thoses fails with a 404 `http://www.youtube.com/watch?feature=fvwp&NR=1&v=mNpUnUBhURY`

* If a conversion fails `convert.py` does not try to know why. It should try to catch something and inform the user about the error

* Use Angular.js

## Licence
AGPLv3+