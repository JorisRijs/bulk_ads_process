#bulk google calendar script

This script is used for importing a large amount of calendar activities for university assignments which are due before a certain time the next day.
The script makes a activity in the calendar for half an hour before the assignment is due so you know you have to hand it in before than.
Also it gives an overview of what is due for the next term.

## Using the script

- clone the repository
- change `Untitled Database.csv` in the following line to the file you want to use<br>
	```with open('Untitled Database.csv', 'r') as data:```
- run the script for the first time
- log in to your google account and allow the script access to your calendar.
- the script should import all of the events from the given csv file and insert it into your calendar.

## File format

The filled in data is example data

|date|assignment|subject|handin date|handin time|
|:---|:---:|:---:|:----:|---:|
|18-05-2020|Assignment network design|OSPF and VPN's|19-05-2020|23:59:00
