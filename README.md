# Project 3: Logs Analysis Project
### by Mostafa Hashish
Logs Analysis Project,part of the Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Explanation
Building an informative summary from logs is a real task that comes up very often in software engineering.

## Technologies used
1. PostgreSQL
2. Writing Python code with DB-API
3. Linux-based virtual machine (VM) Vagrant

## Project Requirements
Reporting tool should answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## How to view the project
This project makes use of Udacity's Linux-based virtual machine (VM) configuration which includes all of the necessary software to run the application.
1. Download [Vagrant](https://www.vagrantup.com/) .
2. Download [Virtual Box](https://www.virtualbox.org/) . 
3. Clone this repository .
4. Download the news.sql (extract **newsdata.zip**) and news.py files from the respository and move them to vagrant directory.

#### Run these commands from the terminal in the folder where vagrant is installed in: 
1. ```vagrant up``` to start up the VM.
2. ```vagrant ssh``` to log into the VM.
3. ```cd /vagrant``` to change to your vagrant directory.
4. ```psql -d news -f newsdata.sql``` to load the data and create the tables.
5. ```python3 news.py``` to run the reporting tool.

## Views used
#### total
````sql
CREATE VIEW total AS
SELECT status,time ::date   
FROM log;
````
#### failed_request
````sql
CREATE VIEW failed_request AS
SELECT count(*) AS num,time
FROM total
WHERE status = '404 NOT FOUND'
GROUP BY time;
````
#### all_requests
````sql
CREATE VIEW all_requests AS
SELECT count(*) AS num,time
FROM total
WHERE status = '404 NOT FOUND'
  OR status = '200 OK'
GROUP BY time;
````
#### percentagecount
````sql
CREATE VIEW percentagecount AS
SELECT all_requests.time,
       all_requests.num AS no_all,
       failed_request.num AS no_failed,
       failed_request.num::double precision/all_requests.num::double precision * 100 AS per_failed
FROM all_requests,failed_request
WHERE all_requests.time = failed_request.time;
````# Logs-Analysis
