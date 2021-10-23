# fishing-bot

Fishing bot that uses pixel diffing of sequenced images to approximate position of bobber. Has roughly a 98% accuracy.

## Start
```sh
pip install -r .requirements.txt
python main.py
```

## Run detection logic against screenshots for testing
```sh
python debug.py
```
### Add new test images
```sh
python collect_samples.py
```
* Then a screenshot will be taken and you need to crop the bobber.
* The filename will be saved into a samples folder with the bobber position as the filename, for asserting success of the locator logic

## Disclaimer

This fishing bot was created as an experiment to play around with image transforms. It is intended purely for learning and I don't take any responsibility for your use of it.
