# spoiler-free-sliggy-vods
This is a flask app that uses the selenium webscraper to get links to Sliggy's vods without displaying any information that would spoil the results of the games.
It requires Python and Firefox to be installed on your computer (it used to work with Chrome but a Chrome update broke it)
You may want to create a virtual environment to install the packages but it is not necessary. 
To use, assuming you have python installed already, simply open the project folder in the command line and run this command:  
pip install -r requirements.txt  
(pip3 install -r requirements.txt on mac)  
to install the required packages  
then use  
flask run  
to start the app  
copy paste the server flask tells you it is running on into your browser and you are good to go!
