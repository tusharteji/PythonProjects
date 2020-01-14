# IMDB Robot Rating

## Project Introduction
This project uses Selenium web driver for Python to automate the creation of new IMDB
accounts and rate any desired movie on the loop. The script is designed to pull out names
from the text file `names.txt` one by one and create an IMDB user account with the respective
name and rate a particular movie with the desired rating. This goes on for all the names in
text file. This project is only for learning purposes. Wrongful use of this script by any
third person or party is not my responsibility.

## Requirements
In order to run this script on your local machine, you will need to install `Selenium` module.
To install `Selenium`, just run the following command on your console/terminal:

```
pip install selenium
```

For Selenium web driver to work, you'll need a web driver such as *chromedriver* which can
be downloaded from [here](https://chromedriver.storage.googleapis.com/index.html?path=2.38/).
Download the one specific to your OS. Unzip it and copy the executable file and paste it in the
same folder as the script `main.py`.

## How to Run the Code
Before you run the code, add the movie name you want to target. In line 6, replace the
comment string with the movie name and assign it to the variable `movie_name`. The current
code is designed to give a star rating of 10 everytime. You can change this by changing the
index to the anchor tag *a* from 10 to any number from 0 to 10 as per your requirement. That's
it! You're good to go. Run the following command to exectue the program:

```
python main.py
```

## Limitations
Since this is a robotic way of repititive accounts registrations, IMDB will sense it after a
few iterations and will start asking to enter *CAPTCHA* during the account creation. Handling
such scenario and situations such as *Internet stopped working* is beyond the scope of this
project.
