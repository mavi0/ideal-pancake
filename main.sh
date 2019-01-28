export PATH=$PATH:~/.local/bin
python3 scrape.py
python3 6h.py
python3 metoffice.py
killall firefox
killall geckodriver
