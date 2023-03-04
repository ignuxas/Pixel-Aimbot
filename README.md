# Pixel-Aimbot
An app that reads your screen and snaps your mouse to certain color of pixels.

This app is designed to lock onto enemies on the screen without reading the game's memory. It works by analyzing the screen in real-time, identifying the brightest pixels, and calculating the middle of those pixels to determine the location of enemies. This process is repeated more than 240 times per second, allowing the app to provide fast and accurate tracking of enemies.

Demonstration on how it works: https://www.youtube.com/watch?v=AZhiZTF3tSw

## Install requirements:

### This app requires Python 3.x.x
```
pip install -r requirements.txt
```

## How to use:
Firstly, if you want to change any settings, open the app.py file in any code editor and change the settings.

When you are satisfied with your chosen settings:
1. Open command prompt
2. ```cd``` into the app's directory
3. ```python app.py```, if that doesn't work: ```python3 app.py```
