## The purpose of this project is as follows:
This program takes data from several reports and merges it using business logic to procedurally audit CUNY College Assistant annual leave time and ensure accurate and timely payouts.
## Here's some back story on why I needed to build this:
At the end of every fiscal year, there is a short window of time between receivcing the last timesheet from each employee in this group and when annual leave calculations must be completed and sent to the state to be paid out. While our proprietary software should do this automatically, there are sometimes additional considerations that it can't accommodate, such as staggered service in a given fiscal year, multiple department employment instnaces, or an undeclared employment history in the title, so this software fills in the gaps.
## This project leverages the following libraries:
matplotlib, pandas
## In order to use this, you'll first need do the following:
A user must have access to CF. A user must have access to SOTA PR-Assist. A user must understand the business rules of classified hourly employees sot hat they can error-check the output in the event that any contract has been updated. 
## The expected frequency for running this code is as follows:
As Needed