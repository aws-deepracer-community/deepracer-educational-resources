# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [markdown] id="XVbNrlXzsdf5"
# # Deepracer winner counter
#
# <img src="./img/0_dr_evo_360.gif" alt="EVO car" width="250">
#
# ## AWS DeepRacer
# AWS DeepRacer is a 1/18th scale autonomous race car but also much more. It is a complete program that has helped thousands of employees in numerous organizations begin their educational journey into machine learning through fun and rivalry.
#
# Visit [AWS DeepRacer page](http://deepracer.com/) to learn more about how it can help you and your organization begin and progress the journey towards machine learning.
#
# Join the [AWS Machine Learning Community](http://join.deepracing.io/) to talk to people who have used DeepRacer in their learning experience.
#
# ## Prizes
#
# AWS offer two types of prizes in the Pro Division of AWS:
# 1.  First Prize: AWS DeepRacer Championship qualification (24 total, 3 per month),
# 1.  Second Prize: AWS DeepRacer EVO (80 total, 10 per month),
#
# But not everything straight forvard. Good racer could not get two cars or go win two slots in the Championships. There is "Prize condition": Each participant may receive a maximum of 1 of each prize type during the 2021 season.
#
# Let's try and identify the winners using Python, Pandas and Jupyter Notebook.
#
# ## Data source
#
# Fetching the data for this task could be a labour intensive task. There is no official DeepRacer API available.
#
# Luckily Jochem Lugtenburg, a developer, AWS Community Builder and a DeepRacer expert in the AWS Machine Learning Community, has prepared a project gathering the data and exposing it to everyone in a GitHub repository: [deepracer-race-data](https://github.com/aws-deepracer-community/deepracer-race-data). We will use final race data for each month from this project.
#
# ## Data preparation
#
# Let's import needed dependencies and load the data:

# + id="yEfUcMikGydf"
import pandas as pd
import numpy as np
from IPython.display import display, HTML

import urllib.request
from urllib.error import HTTPError

pd.set_option("display.max_rows", None, "display.max_columns", None)

# + [markdown] id="rm6umRqRx21y"
# There is a file [leaderboards.csv](https://github.com/aws-deepracer-community/deepracer-race-data/blob/main/raw_data/leaderboards/leaderboards.csv )  in the GitHub repository that contains information about all competitions: start date, end date, number of participants, rules, etc. We need to find and extract information about this season races. Let's take a closer look to this summary CSV file:

# + colab={"base_uri": "https://localhost:8080/", "height": 496} id="9aeCKTfAUn9h" outputId="cfb52c84-ef87-4d8b-88af-a44eea94a163"
df_leaderboards = pd.read_csv('https://raw.githubusercontent.com/aws-deepracer-community/deepracer-race-data/main/raw_data/leaderboards/leaderboards.csv')
df_leaderboards.head()

# + [markdown] id="R5UZ8ZaPUvWM"
# You need to manually add data to variable **month_races** which is colomn "Name" from df_leaderboards: [leaderboards.csv](https://github.com/aws-deepracer-community/deepracer-race-data/blob/main/raw_data/leaderboards/leaderboards.csv ) 

# + id="g2C-_KtVEg6E"
months_races = ['March Qualifier', 'April Qualifier', 'May Qualifier', 'June Qualifier', 'July Qualifier', 'August Qualifier', 'September Qualifier', 'October Qualifier']

race_type = ['HEAD_TO_HEAD_RACING', 'TIME_TRIAL', 'OBJECT_AVOIDANCE']

# Get Arn URLs according to race type: HEAD_TO_HEAD_RACING – month qualifier leader board and OBJECT_AVOIDANCE – final race
month_leaderboard_arn = df_leaderboards.loc[(df_leaderboards['Name'].isin(months_races)) & (df_leaderboards['RaceType'] == "HEAD_TO_HEAD_RACING")]['Arn'].values
month_final_arn = df_leaderboards.loc[(df_leaderboards['Name'].isin(months_races)) & (df_leaderboards['RaceType'] == "OBJECT_AVOIDANCE")]['Arn'].values

# Next we need to get raw data for final races and month qualifier leader. We put dataframes to lists: one for month qualifier and second for winners
path = "https://raw.githubusercontent.com/aws-deepracer-community/deepracer-race-data/main/raw_data/leaderboards/"
suffix = "/FINAL.csv"

list_end_of_month=[]
for arn_leaderboard in month_leaderboard_arn:
  try: 
    list_end_of_month.append(pd.read_csv(path+month_leaderboard_arn[np.where(month_leaderboard_arn == arn_leaderboard)[0][0]].replace(":", "%3A")+suffix))
  except urllib.error.HTTPError as err:
    list_end_of_month.append(pd.DataFrame(columns=['Alias', 'UserId', 'Rank', 'Month']))


list_finale=[]
for arn_win in month_final_arn:
  try:
    list_finale.append(pd.read_csv(path+month_final_arn[np.where(month_final_arn == arn_win)[0][0]].replace(":", "%3A")+suffix))
  except urllib.error.HTTPError as err:
    list_finale.append(pd.DataFrame(columns=['Alias', 'UserId', 'Rank', 'Month']))
    pass


# + [markdown] id="m0N50FYpz_xj"
# You can mention construction 
# ```
# try:
# except urllib.error.HTTPError as err:
# ```
# that was used due to Final october race still upcoming at the time of writing this article. Because of that the file FINAL.csv was not available and we protected ourselves by adding an empty dataframe so that we didn't have to handle a missing entry in a list in code that followed
#
#
# Let's have a quick look at what information we can get from the repository:

# + colab={"base_uri": "https://localhost:8080/", "height": 224} id="HFFcFVmA0IDt" outputId="53d2b667-2834-4a18-e911-52aa664771e5"
# Index 0 is foe March, respectively 1 is for April etc.
list_finale[0].head()

# + [markdown] id="K8PvNmMB0Rsl"
# In reality we only care about three pieces of data: Alias, Rank and and UserId.
#
# Let's have a look at a narrowed dataset:

# + colab={"base_uri": "https://localhost:8080/", "height": 204} id="Lmr19H5Z0ojI" outputId="b22d79ba-91b2-430c-9199-fda0e946e791"
list_finale[0][['Alias', 'UserId', 'Rank']].head()

# + [markdown] id="0kgjmRqczJFl"
# ## Finalists
#
# Let's start with the finalists. After each month's Pro Division race, top 16 racers who have not yet qualified into the championships compete in a finale race. Top 3 racers from each such race qualify into the championships.
#
# `df_month_finale` dataframes above hold results for those races. They are sorted by Rank which makes it easier for us as we don't have to think about reordering the records.
#
# To build a list of winners, for each month we need to take the top 3 racers and append them to a list of racers. Luckily we don't neet to worry about duplicate racers either as none of the previous winners take part in the finales anymore.
#
# ![DeepRacer.jpeg](./img/1_winners_selection.jpeg)
#
# This is our method to determine the finalists:
#
#
#
#
#
#

# + id="kq2xs14g2N9Q"
Month = ['March', 'April', 'May', 'June', 'July', 'August', 'September', 'October']

def championship_racers():
  df_winners = pd.DataFrame(columns=['Alias', 'UserId', 'Rank', 'Month'])

  for idx, finale in enumerate(list_finale):
    df_winners = df_winners.append(finale[['Alias', 'UserId', 'Rank']].iloc[:3]).reset_index(drop=True)
    df_winners['Month']= df_winners['Month'].fillna(Month[idx])
  return df_winners


# + [markdown] id="oQCpsj4X5iXb"
# A few words on what we did here:
# * We've prepared an empty Pandas dataframe with columns
# * We enumerated over the list of dataframes - `enumerate` method iterates over the elements of a list but it also provides an index of the element in that list. This helps us add the month name as an extra column
# * We've added a month column, just to know in which month this person qualified
# * We've simply appended top three rows from each finale dataframe into the winners dataframe. We used `iloc` to limit the number of rows
# * We've reset the index values. Without this the new dataframe with winners would have the index all messed up
# * To add the months we use a `fillna` method. It's pretty handy as it only sets values where they are missing
#
# Let's see the results:

# + colab={"base_uri": "https://localhost:8080/", "height": 793} id="zRX52KB65hVF" outputId="bb86bbf4-2c75-4294-a936-65261a40224b"
championship_racers()

# + [markdown] id="LuvC44048f9T"
# Let's imagine that the month just finished and the final race have not occure yet but we want to see who will compete in it. Let's see who compete in October final race:

# + colab={"base_uri": "https://localhost:8080/", "height": 545} id="ookSbIcP8xUh" outputId="bcbd1f80-c99f-48c2-9987-4d89b83a5a96"
list_end_of_month[7][['Alias', 'UserId', 'Rank']].head(n=16)


# + [markdown] id="AZhvydqA9Ep5"
# Well, this is wrong - I can see people who have already qualified into the championships on this list.
#
# To determine the finale racers we need to use October race results, but we first need to remove those who already qualified. Let's try that:

# + id="xL0vGiMy94-S"
def october_finale_racers():
  championship_racers_so_far = championship_racers()[['Alias', 'UserId', 'Rank']]
  return list_end_of_month[7][['Alias', 'UserId', 'Rank']].append(championship_racers_so_far).drop_duplicates('UserId', keep='last').reset_index(drop=True).head(n=16)


# + [markdown] id="aUHUo4AN-fln"
# We've use a new method: `drop_duplicates`. It takes values of specified column and by default keeps the first one and discards the rest. We used a little trick here - by putting the championship racers at the end and telling the `drop_duplicates` to only keep the last appearance we make sure that if the they raced in October, their entry will be dropped, leaving only those who can join the top finale race.
#
# UserId is a unique and unchangeable identifier for each racer. Starting this season users can change their Aliases (which comes as a great relief to those racing under their often very creative model names) so trying to enforce uniqueness using the Alias values would not work.
#
# Let's run this:

# + colab={"base_uri": "https://localhost:8080/", "height": 545} id="otId0XR8-7NW" outputId="623bc391-5b01-4109-8d9a-a6ae0bab298f"
october_finale_racers()


# + [markdown] id="G_Ub4pCP__L8"
# ## AWS DeepRacer Evo winners
#
# Now time for the Evo winners. Here rules get a little bit more complicated. As written above, it is top 10 racers that win the car and only once. In March we care about top 10 finale racers. In April - some from finale, but maybe we have someone from below the top 16 that wins one?
#
# We need to take the month's race results into consideration but also the fact that someone from places 10-16 in that race might be in top 10 in the finale.
#
# Let's have a look at the code and then we'll look at what's going on in here:

# + id="sIs-yQ1kXgxl"
def car_winners():
  df_car_winners = pd.DataFrame(columns=['Alias', 'UserId', 'Rank', 'Month'])
  for idx, list_file in enumerate(list_end_of_month):
    df_car_winners = df_car_winners.append(list_finale[idx][['Alias', 'UserId', 'Rank']]).append(list_file[['Alias', 'UserId', 'Rank']]).drop_duplicates('UserId').reset_index(drop=True).iloc[:(idx+1)*10]
    df_car_winners['Month']= df_car_winners['Month'].fillna(Month[idx])
  return df_car_winners



# + [markdown] id="nVlEnnApDp-9"
# Let's focus at this bit as it's the most important here:
#
# ```
# df_car_winners.append(list_finale[idx][['Alias', 'UserId', 'Rank']]).append(list_file[['Alias', 'UserId', 'Rank']]).drop_duplicates('UserId')
# ```
#
# For each month we take the car winners so far, append the finale results to it, then the month race results, and drop the duplicates leaving only the first occurrence of a UserId value. This means that if someone is already a car winner, their entries will be removed from finale and month race results. Likewise, if they were finale racers, their month race results will be removed.
#
# Effectively this means tha we build a list containing all the car winners so far and a list of rank-ordered performers in a given month who have not yet won a car. All we need to do now is to drop everyone except of the top ten for a given month. Since each month the list is growing, we perform `.iloc[:(idx+1)*10]`.
#
# Let's see the results:

# + colab={"base_uri": "https://localhost:8080/", "height": 1000} id="twKmMHjGeMSX" outputId="fd6c2b7f-a523-4c4b-fa93-95c484218f0e"
car_winners()

# + [markdown] id="MJJzVX8O0xPm"
# ## Wildcard race winners
#
# AWS always give a last minute opportunity to qualify. Normally this would be a live race at the re:Invent conference but since everything is taking place virtually, so is this Wildcard race. Top five participants take part in the championships, but we need to sift out those who race but already had their places secured.
#
# The race just finished and we wanted to know who qualified. We can either add FINAL.csv in the months_races list or **get raw** information from the Github table. Click "raw" and copy URL: 
# <img src="img/2_raw_file_finding_on_github.png" />
#
# Now all that's left is to load the file, remove the finalists so far and list top five racers:

# + id="GINwMp3Y0v7r"
wildcard_open = pd.read_csv("https://raw.githubusercontent.com/aws-deepracer-community/deepracer-race-data/main/raw_data/leaderboards/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard/08db3006-f491-48b4-a238-926c6465e5d8/FINAL.csv")

def wildcard_qualifier(df_wildcard):
  winners = championship_racers()
  wildcard_5 = df_wildcard[['Alias', 'UserId', 'Rank']].append(winners).drop_duplicates('UserId', keep='last').reset_index(drop=True).head(n=5)
  wildcard_5['Month']= wildcard_5['Month'].fillna("wildcard")   
  return wildcard_5


# + [markdown] id="HzPAJnYq3NnO"
# Let's see who quilified through the Wildcard race:

# + colab={"base_uri": "https://localhost:8080/", "height": 204} id="ha-r0DJy3IDE" outputId="c5f1fbef-330b-46ab-f864-8ea404112c65"
wildcard_qualifier(wildcard_open)

# + [markdown] id="6EhOu_xFFU5W"
# ## Limitations
#
# There are things we cannot verify ourselves that may greatly influence the above results. AWS perform eligibility checks on those racers and the racers themselves need to claim the prize. This means that racers can get removed from this list and we have no way do find out.
#
# ## Source code
#
# This article has been prepared as a Jupyter Notebook which we have shared on GitHub. You can download it yourself and play with it a little here: [https://github.com/mokoron/deepracer.git](https://github.com/mokoron/deepracer.git)

# + [markdown] id="iFSlASw3jmo7"
# # SageMaker 
#
# I guess you want to play aroud with notebook. You can easily do it by running this into AWS Sagemaker. 
#
# First, login into your ASW account and navigate to Amazon SageMaker:
#
# ![How to find SageMaker in AWS Console](./img/3_sagemaker_in_aws_console.png)
#
# Navigate to Notebook – Notebook Instancies and Create notebook instance (orange button on a right top corner). Choose a name for Notebook instance other parameters you can leave as default value.
#
# ![Creating a new SageMaker Notebook](./img/4_new_sagemaker_notebook.png)
#
# Next, in the Git Repositories section select "Clone a public Git repository to this instance only" and provide the URL of this article's repository: 
# ![Selecting a public repository](./img/5_clone_git_repository.png)
#
# Wait a couple of minutes for Instance to be created.
#
# Now you can open the notebook and make changes to it. If you get an error about kernel not being found, select conda_python3
#
# Do not forget to Stop Notebook instance when you finish to prevent unexpected billing. **YOU WILL GET BILLED IF YOU DO NOT**
#
# ![Stopping a SageMaker Notebook to prevent costs](./img/6_stop_sagemaker_notebook.png)

# + id="CAHw5M5oGNZB"

