# diyha-clock
Adafruit's seven-segment I2C LED backpack device used as a simple clock controlled by MQTT subscribed messages. The Python application responds to specific information based on application topics, e.g. MQTT Broker subscribe/publish. This application is one of several general classes in my *do it yourself home automation system* (**DIYHA**). Each python DIYHA application is hosted on a Raspberry Pi Zerp W server (raspbian lite). 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django)
[![linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)

> Live demo [_here_](https://www.example.com). <!-- If you have the project hosted somewhere, include the link here. -->

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Architecture](#architecture)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
- Provide general information about your project here.
  - This is one of several classes used in my home automation system (**DIYHA**). I've used OOP and MVC concepts in my DIYHA system. 
- What problem does it (intend to) solve?
  - I wanted to implement a simple clock that automatically resets after a power outage. We used to manually update each clock in the house. A unix based solution automatically updates time on boot.
- What is the purpose of your project?
  - My home automation system contains environment sensors, motion sensors, LED clocks, light switches, emergency sirens, a django web server, interfaces to and a mosquitto MQTT broker. I added a motion sensor as a security measure and an 8x8 LED for art and messaging. These are both implemented as seperate unix processes.
- Why did you undertake it?
  - This was a fun project to learn about python, Raspberry Pi, Arduino processors, hardware and more.
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->

## Technologies Used
- python - version 3.7.3
- Adafruit libraries like adafruit-blinka

## Features
List the ready features here:
- Displays time in several formats, e.g., 12 hour or 24 hour, indicates am/pm and alarms, and dims or brightens based on MQTT topics
- Handles the basic **diy/system/who** function to show the IP address of the device.
- Reports on status and diagnostic information by LOGGING application specific informatino message.
- Code passes pylint with a score of 10.0

## Screenshots
Not applicable.
<!-- ![Example screenshot](./diyhadiagram.png)-->
<!-- If you have screenshots you'd like to share, include them here. -->

## Architecture
![Example screenshot](./diyhadiagram.png)
<!-- If you have screenshots you'd like to share, include them here. -->

## Setup
What are the project requirements/dependencies? Where are they listed? A requirements.txt or a Pipfile.lock file perhaps? Where is it located?
- A requirements.txt file contains the dependencies
- IMPORTANT: a MQTT message broker is required. I recommend mosquitto.

Proceed to describe how to install / setup one's local environment / get started with the project.
```
git clone https://github.com/parttimehacker/diyha-clock.git
cd diyha-clock
sudo pip3 install -r requirements.txt
```
- Install as a systemd application to start at boot 
```
./systemd_script.sh diyha-clock
```
- start, stop and status bash aliases are also available
```
cd
source .bashrc
diyha-clock.start
```

## Usage
How does one go about using it?
Provide various use cases and code examples here.

- The clock starts at boot time. Not user interaction is required. 
```
from pkg_classes.whoview import WhoView
```
- initialization of the view controller
```
# get the command line arguements
CONFIG = ConfigModel(LOGGING_FILE)

# setup web server updates
DJANGO = DjangoModel(LOGGING_FILE)
DJANGO.set_django_urls(CONFIG.get_django_api_url())

# Set up who message handler from MQTT broker and wait for client.
WHO = WhoView(LOGGING_FILE, DJANGO)
```
- provide MQTT client
```
WHO.set_client(CLIENT)
```
- process diy/system/who topic subscription
```
client.subscribe("diy/system/who", 1)
```
- handling diy/system/who messages


## Implementation Status
![Status](https://progress-bar.dev/80/?title=progress)


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Further refactoring to more generalize the classes

To do:
- Integrate into other DIYHA applications and repositories
- Develop a new installation process for seperate repositories

## Acknowledgements
Give credit here.
- This project was inspired by...
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to...


## Contact
Created by [@parttimehacker](http://parttimehacker.io/) - feel free to contact me!
### Repository Stats
![Your Repository’s Stats](https://github-readme-stats.vercel.app/api?username=parttimehacker&show_icons=true)
### Repository Languages
![Your Repository's Stats](https://github-readme-stats.vercel.app/api/top-langs/?username=parttimehacker&theme=blue-green)
### HITS
![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https://github.com/parttimehacker)


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
