# Project-4-Data-Warehouses

### Introduction

Sparkify, a music streaming app want to move their processes and data into the cloud, as their userbase and song database has grown. Their data consists of a directory of JSON logs which shows user activity on the app and also JSON metadata about songs. This currently sits in S3. 

### Project
The main focus of the project is to build an ETL pipeline that extracts the above data in S3, stages them in Redshift and transforms data into a set of dimensional tables for the analytics team to keep driving insights from the data. 

### Schema
#### Fact Table

**Songplay** – Record event data associated with song plays. Columns include \
Songplay_id \
Start_time \
User_id \
Level \
Song_id \
Artist_id \
Session_id \
Location \
User_agent

#### Dimension tables
**Users** \
User_id \
First_name \
Last_name \
Gender \
Level 

**Songs** \
Song_id \
Title \
Artist_id \
Year \
Duration 

**Artists** \
Artist_id \
Name	\
Location \
Latitude \
Longitude \
Time 
 
**Start_time** \
Hour \
Day \
Week \
Month \
Year \
Weekday 


