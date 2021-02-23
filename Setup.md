# Setup 
1. Clone the reponsitory from terminal: `git clone https://github.com/Ravveni/PizzaPartyBot.git`
2. (Suggested) In project directory, create a virtual environment named 'PPBEnv': `python3 -m venv PPBEnv`
3. Install requirements: `pip3 install -r requirements.txt`
4. Get proper Geckodriver web driver for system

> #### Mac Geckodriver
> [Download the latest driver here](https://github.com/mozilla/geckodriver/releases)
>  
> #### Raspberrian Geckodriver
> [Last viable release from Mozilla for ARM processors](https://github.com/mozilla/geckodriver/releases/download/v0.22.0/geckodriver-v0.22.0-arm7hf.tar.gz)

5. From downloaded geckodriver folder, move executable into PATH: `sudo mv geckodriver /usr/local/bin/`

6. TBF...

## Other System Considerations
### Mac
There are several `objc` python frameworks that will be added in the process of downloading requirements. These were removed to prevent crashes during setup on Raspberrian.

You will have to grant accessibility and screen sharing permissions when asked for selenium and the image recognition to work properly.

### Raspberrian
There are several missible libraries that will need to be installed:

```
sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
```
