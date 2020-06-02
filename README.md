
Welcome to this lil' instagram scarping tool

## TODO
- Pick up shop and use Instagram's Graph API (for those with accepted keys)
- Figure out way to subvert the login force (added 2020)
- TEST scrape in python 2.x

## GYFOOT Scrape

- This tool was created to assist a friend in need of training images for a CNN he was building
- Doubled as an opportunity to teach him how selenium works
- Updates to Instagram's web experience and their Graph API have rendered this currently broken

## Quick Start:
- Run `instaScrape_py3.py` however you like, follow input prompts

## Core Packages

`pip install beautifulsoup4 selenium requests webdriver-manager`  
or  
`pip install -r requirements.txt`

## Venv cheat sheet

Man & Linux:  
`python3 -m pip install --user virtualenv`  
`python3 -m venv <env_name>`  
`source <env_name>/bin/activate`  

Windows: (does not work on WSL 1)  
`python3 -m pip install --user virtualenv`  
`python3 -, venv <env_name>`  
`.\env\Scripts\activate`  


To exit the venv:  
`deactivate`