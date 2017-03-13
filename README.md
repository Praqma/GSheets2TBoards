# GSheets2TBoards
Small dockerized python script to convert a google sheet into a Trello board

## Usage:

1) Create a copy of the 'Example Template' on Google and fill it in based on the instructions in it.
https://docs.google.com/spreadsheets/d/1Q_aOqbvPPiDeovl-eDC7bKdurMq1M_BQyY9tca1i-lg/edit#gid=372680571

2) Run this docker command

	docker run -it praqma/gsheets2tboards:0.1.1 python ./main.py --noauth_local_webserver


You need to have read access to the sheet importing from.
After the import, you have a personal Trello board.
