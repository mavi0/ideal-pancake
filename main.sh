export PATH=$PATH:~/.local/bin
echo "Gathering 6H data"
python3 6h.py
echo "Gathering IG data"
python3 scrape.py
sudo killall firefox
sudo killall geckodriver

cp results/*.json /var/www/html/json/
cp results_6H/*.json /var/www/html/json/
