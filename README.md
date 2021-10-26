# Deepracer winner counter

![EVO car](https://d1.awsstatic.com/deepracer/Evo%20and%20Sensor%20Launch%202020/evo-spin.fdf40252632704f3b07b0a2556b3d174732ab07e.gif)



## AWS DeepRacer
AWS DeepRacer is a 1/18th scale autonomous race car but also much more. It is a complete program that has helped thousands of employees in numerous organizations begin their educational journey into machine learning through fun and rivalry.

Visit [AWS DeepRacer page](http://deepracer.com/) to learn more about how it can help you and your organization begin and progress the journey towards machine learning.

Join the хAWS Machine Learning Community(http://join.deepracing.io/) to talk to people who have used DeepRacer in their learning experience.

## Rules
According to the [rules](https://d1.awsstatic.com/AWS%20DeepRacer%20League%202021%20Official%20Rules%203_1.pdf), once you quilify to the PRO Division you can try to win EVO Physical car and even the main prize: first prize is a trip to re:Invent 2021 in Las Vegas, NV USA.

1.  First Prizes (24 total, 3 per month),
1.  Second Prizes (80 total, 10 per month),
1.  Third Prizes (3,000 maximum, top 10% of each Open division per month): The winner of each First and Second Prize will also receive a Third Prize.

But not everything straight forvard. Good racer could not get two cars or go to the re:Invent 2021 with a plus one. There is "Prize condition": Each participant may receive a maximum of 1 of each prize type during the 2021 season.

The logic of getting prise is the follows: first 16 racer each month race for the First Prize. 10 of them get an EVO Physical car. In case of all of 16 participants already won a car we pay attention on month leaderboard and pick next racer who have not win a car yet till we get 10 winners over all.

So if you wold know if you are illegible to get a car or participate into final monthly race, you can use `<Deepracer_league.ipynb>` script.

## How to use

First of all, you should fill in data for month leaderboards for final race and final for monts Qualifier. 

Next you'll find several functions in `<Deepracer_league.ipynb>` script:
* **car_winners_new** – all racers who already win an EVO this season (Second Prizes);
* **winner** – all racers who already get a First Prizes – a trip to re:Invent;
* **sixteen_applicants** – current month applicant for final month race;
* **car_applicants** – current monts an EVO car applicant.
