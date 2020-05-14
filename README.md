<p align="center">
  <img width="200" height="200" src="/gmit.png/">
</p>


<h1 align="center" ><br>Final Year Project<br></h1>

<br>
<br>
<p align="center">
  <img width="200" height="200" src="/aiCompanion.jpg/">
</p>
<p align="center">
  <img width="200" height="200" src="/logo.png/">
</p>

<h4 align="left">BEng in Software and Electronic Engineering<br><br>
Student Name: Padraig O Cosgora<br>
Student Number: G00311302<br>
Supervisor: Brian O’ Shea<br>
Project Engineering<br>
Year: 4<br>
</h4>

<p>&nbsp;</p>

<h2 align="left"><b>Introduction</b></h2>
My motivation for choosing this project stems back to when I was at Intel and took part in a Kaggle 
competition; it's a Machine Learning website with learning resources and competitions. I loved it. We ended up 
finishing 2nd place. I wanted to expand my knowledge base in this area by developing and deploying my ML algorithms.

<h2 align="left"><b>Project Description</b></h2>
The AI Companion is a home assistant robot that can autonomously move around the home. It is equipped 
with an HD video camera, enabling the AI Companion to use the power of machine learning to avoid collisions and 
recognise objects, such as a person or a pet. The AI Companion can also be controlled remotely via a web application, 
offering you live data from your home and a sense of security when you're away from home. The web interface also runs a 
live machine learning model, checking up on your financial portfolio by returning all positive and negative sentiment 
concerning any selected companies.  The AI Companion can also be paired with a smart assistant, such as Google Home or 
Alexa, giving you an AI smart companion.

<h2 align="left"><b>Project Market </b></h2>

The idea is to build upon the increasing success of home assistants and automated assistance products such as the Roomba
 (the autonomous vacuum) or the auto-mowers that are also quite popular. By offering an autonomous solution, homeowners 
 will no longer have to purchase a smart assistant in each room to gain full benefits of the system. Also, the home 
 security option provides peace of mind to consumers when they're away from home. As you can see from the graph on the 
 screen, just in the last year between 2018-2019, total sales of smart assistants rose by 35%. In a recent study from 
 ABI Research, the coronavirus has seen a further increase by as much as 30% compared to this time last year. Also, the 
 reason for deploying machine learning algorithms "on the edge" is that most ML algorithms are run online by a cloud 
 service. However, studies by Pew Research Center in 2019 found that 81% of people say the potential risks they face 
 because of data collection far outweigh the benefits of the service.

<h4><b>Skills & Technologies</b></h4>

<h4><b>Flask (Python web sever)</b></h4>   

Used to serve the AI Companion web application.
<h4><b>MQTT:</b></h4>
CloudMQTT is utilised as a broker for the publishing and subscribing of data from the sensors listed below.
<h4><b>Machine Learning : Obstacle Avoidance</b></h4>
The AI Companion can be configured to learn it's new surroundings and any obstacles that may lie in its path – this can 
be done by taking a series of images of the obstacle's and classifying those images as blockages. Images will also be 
taken on the AI Companion when it's free to roam, and these two datasets are used as classifiers to apply transfer 
learning to a neural network that will train a machine learning model to recognise those obstacles in real-time going 
forward.
<h4><b>Machine Learning : Object Detection</b></h4>
Utilising the SSD-Mobilenet-v2 model which is trained on the MS Coco dataset of about 90 objects.
<h4><b>Machine Learning : Financial Sentiment Analysis</b></h4>
RandomForest classifier trained on data containing headlines and sentiment, returned a accuracy of ~93% on test data. 
This model is then used on the latest news to provide an overall summary of sentiment of an entire stock portfolio.
<h4><b>Sensors:</b></h4>
IR Sensor, BMP280
<h4><b>Hardware</b></h4>
2x Servo Motors, motor driver, Jetson Nano Development board, ESP32
<h4><b>Programming Languages :</b></h4>
C++ (ESP32), Python, Javascript (client-side)
