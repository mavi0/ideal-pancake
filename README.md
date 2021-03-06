# Ignitenet Metrolinq data scraper

Extract JSON from IGNITENET Metrolinq web ui for client monitoring statistics

## Setup Instructions

1. Download this tool with
```bash
git clone https://github.com/mavi0/ideal-pancake.git
cd ideal-pancake/
```
2. Install dependancies
```bash
sudo apt install -y python3 python-pip python3-pip python3-bs4 firefox vim wget screen
pip3 install iperf3 pingparsing bs4 selenium schedule
```
3. Put geckodriver in ~/.local/bin/
```bash
sudo rsync -a geckodriver ~/.local/bin/geckodriver
```
4. Make directory for results and config
```bash
mkdir results/ && mkdir config/
```
5. Get credentials file for the radio. Edit it to include the correct hostname, username and password
```bash
cd config/ && wget https://gist.githubusercontent.com/mavi0/e297397e52cd613f7b96228164000e4e/raw/cdd6b9a256473eba3afe1c6de998946f91360a4b/credentials.json && vi credentials.json
```

## Usage instructions

Simply run:
```bash
 bash main.sh
 ```
The output will be saved to the results directory

To run as a service:
```bash
crontab crontab
```
