# # # ABOUT
# This Python scripts serves as the purpose to create JSON file data items to enter to AWS using specific criteria for Skiin app testing

# # # USE INSTRUCTIONS
# 1. Add all datasets into data folder and make sure data in .csv files are in correct format
# 2. Add userIDs from AWS into userID array
# 3. Change name of files and userID user and click start to generate JSON objects
# 4. Download/open the output.txt file in the folder to see generated JSON objects

##################################################################################################################################

# imports
import pandas as pd
import json
from datetime import datetime, timedelta

# clean file
with open('output.txt', 'w') as f:
  f.truncate(0)

# variables
userID = ["86e97d4b-0a24-495b-a35b-395e9c68e647", "c8b152f4-64d1-4f34-b4ca-c7c6395495c3", "465807e0-34fc-4bfa-8126-ca457417f323", "22d79d85-0784-4a9e-b8ce-737e7801c374", "20adc144-596e-4330-97b5-267f3520acd0", "f6c18f27-ea08-4c96-be2f-52a68e87a6bf"];

rhr = ""
hrv = ""
sleep_score = ""
core_body = ""
breathing_rate = ""
rhrBaseline = "-200"
hrvBaseline = "-200"
sleep_scoreBaseline = "-200"
core_bodyBaseline = "-200"
breathing_rateBaseline = "-200"

rhrMax = "-200"
cbtMax = "-200"
hrvMax = "-200"
rrMax = "-200"
sleepMax = "-200"

rhrMin = "-200"
cbtMin = "-200"
hrvMin = "-200"
rrMin = "-200"
sleepMin = "-200"

sleepDate = "";

counterWeek = 0;
counterDay = 0;
case = 0;

# get data and process

################ USER INTERFACE ########################
userid = userID[3];
df = pd.read_csv('data\Dataset6.csv');
########################################################

# determine dataset case and row allocation
index = df.index
number_of_rows = len(index)
row = 0;

# case 1
if "7-day moving average" in df['Date'].values and "Personal Long-term Range Min" in df['Date'].values:
  case = 1;
  row = number_of_rows - 3;

# case 2
elif "7-day moving average" in df['Date'].values:
  case = 2;
  row = number_of_rows - 1;

# case 3
elif "7-day moving average" not in df['Date'].values:
  case = 3;
  row = number_of_rows;

print(row)
print("Case: " + str(case));
# get columns
date = df['Date'].values;
hrvColumn = df['HRV'].values;
rhrColumn = df['RHR'].values;
sleepScoreColumn = df['Sleep Score'].values;
coreBodyColumn = df['Core Body Temperature'].values;
breathingRateColumn = df['Breathing Rate'].values;

# iterate through data
for i in range(0, row):
  counterWeek += 1;
  counterDay += 1;
  if (case == 1 or case == 2):
    if counterWeek == 7:
      counterWeek = 0;
      seven_day_average = (df[df['Date'] == "7-day moving average"]).values.tolist()[0];
      hrvBaseline = str(seven_day_average[1]);
      rhrBaseline = str(seven_day_average[2]);
      sleep_scoreBaseline = str(seven_day_average[3]);
      core_bodyBaseline = str(seven_day_average[4]);
      breathing_rateBaseline = str(seven_day_average[5]);
    else:
      hrvBaseline = "-200";
      rhrBaseline = "-200";
      sleep_scoreBaseline = "-200";
      core_bodyBaseline = "-200";
      breathing_rateBaseline = "-200";

  if (case == 1):
    if counterDay >= 30:
      minRange = (df[df['Date'] == "Personal Long-term Range Min"]).values.tolist()[0];
      maxRange = (df[df['Date'] == "Personal Long-term Range Max"]).values.tolist()[0];
      hrvMax = str(maxRange[1])
      rhrMax = str(maxRange[2])
      sleepMax = str(maxRange[3])
      cbtMax = str(maxRange[4])
      rrMax = str(maxRange[5])

      hrvMin = str(minRange[1])
      rhrMin = str(minRange[2])
      sleepMin = str(minRange[3])
      cbtMin = str(minRange[4])
      rrMin = str(minRange[5])

    else:
      rhrMax = "-200"
      cbtMax = "-200"
      hrvMax = "-200"
      rrMax = "-200"
      sleepMax = "-200"
      rhrMin = "-200"
      cbtMin = "-200"
      hrvMin = "-200"
      rrMin = "-200"
      sleepMin = "-200"

  rhr = str(rhrColumn[i]);
  hrv = str(hrvColumn[i]);
  sleep_score = str(sleepScoreColumn[i]);
  core_body = str(coreBodyColumn[i]);
  breathing_rate = str(breathingRateColumn[i]);

  # day correction
  timeValue = date[i].split('-');
  sleepDate = str(int(datetime(int(timeValue[0]), int(timeValue[1]), int(timeValue[2]), 9, 0, 0).timestamp())) + str('000');
  longTsForm = str(int((datetime(int(timeValue[0]), int(timeValue[1]), int(timeValue[2]), 9, 0, 0) - timedelta(hours=12)).timestamp())) + str('000');

  JSON = {
    "userId": {
      "S": userid  # from array
    },
    "sleepDate": {
      "N": sleepDate  # from epoch calculator in script
    },
    "baselineMaxLongTermRhr": {
      "N": rhrMax  # same
    },
    "rr": {
      "S": breathing_rate  # from table
    },
    "sleepDuration": {
      "S": "20220"  # don't change
    },
    "baselineMinLongTermSleepScore": {
      "S": sleepMin # don't change
    },
    "hrv": {
      "S": hrv  # from table
    },
    "baselineHrvChannel1": {
      "S": hrvBaseline  # don't change
    },
    "baselineMaxLongTermRR": {
      "S": rrMax  # don't change
    },
    "baselineMaxLongTermHrv": {
      "S": hrvMax # don't change
    },
    "deep": {
      "S": "0"  # don't change
    },
    "baselineMinLongTermRR": {
      "S": rrMin  # don't change
    },
    "cbt": {
      "N": core_body  # from table
    },
    "baselineMinLongTermRhr": {
      "N": rhrMin  # don't change
    },
    "baselineMaxLongTermCbt": {
      "N": cbtMax # don't change
    },
    "rhr": {
      "N": rhr  # from table
    },
    "longTsFrom": {
      "N": longTsForm
    },
    "tossAndTurn": {
      "S": "31"
    },
    "sleepDeterminedStart": {
      "S": longTsForm
    },
    "baselineMinLongTermCbt": {
      "N": cbtMin # don't change
    },
    "sleepTimeLeft": {
      "S": "6300"  # don't change
    },
    "awakeBeforeSleep": {
      "S": "0"  # don't change
    },
    "hrvChannel1": {
      "S": hrv  # hrv value
    },
    "sleepTimeRight": {
      "S": "0"  # don't change
    },
    "baselineMinLongTermHrv": {
      "S": hrvMin # don't change
    },
    "awake": {
      "S": "1350"  # don't change
    },
    "baselineRhr": {
      "N": rhrBaseline  # change on 7th day
    },
    "longTsTo": {
      "N": sleepDate
    },
    "createdAt": {
      "N": sleepDate
    },
    "light": {
      "S": "19620"  # don't change
    },
    "baselineSleepScore": {
      "S": sleep_scoreBaseline  # change on 7th day
    },
    "durationDataUploaded": {
      "N": "43200000"  # don't change
    },
    "sleepDeterminedEnd": {
      "S": "1637071200000"  # don't change
    },
    "sleepScore": {
      "S": sleep_score  # from table
    },
    "sleepTimeFront": {
      "S": "0"  # don't change
    },
    "baselineRR": {
      "S": breathing_rateBaseline  # change on 7th day
    },
    "updatedAt": {
      "S": ""  # don't change
    },
    "baselineHrv": {
      "S": hrvBaseline  # change on 7th day
    },
    "sleepTimeBack": {
      "S": "14700"  # don't change
    },
    "rem": {
      "S": "600"  # don't change
    },
    "sleepQuality": {
      "S": "93.7413073713491"  # don't change
    },
    "sleepStartedAt": {
      "N": longTsForm
    },
    "baselineCbt": {
      "N": core_bodyBaseline  # change on 7th day
    },
    "baselineMaxLongTermSleepScore": {
      "S": sleepMax  # don't change
    }
  }
  JSON = json.dumps(JSON)
  print(JSON)
  with open('output.txt', 'a') as f:
    f.write(str(JSON) + '\n\n')