export PATH=$PATH:~/.local/bin
python3 6h.py
python3 scrape.py
sudo killall firefox
sudo killall geckodriver

cp results/*.json /var/www/html/json/
cp results_6H/*.json /var/www/html/json/
