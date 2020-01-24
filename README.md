# GSheets2TBoards
Small dockerized python script to convert a google sheet into a Trello board

## Usage:

1) Create a copy of the 'Example Template' on Google and fill it in based on the instructions in it.
https://docs.google.com/spreadsheets/d/1Q_aOqbvPPiDeovl-eDC7bKdurMq1M_BQyY9tca1i-lg/edit#gid=372680571

2) Run this docker command

	docker run -it praqma/gsheets2tboards:latest


You need to have read access to the sheet importing from.
After the import, you have a personal Trello board.

### How to create Google OAuth client
The credentials in this project will only work on `eficode` GSuite Google accounts. If you want to run it within your own organisation, you need to do the following:
-  Go to [the Google API Developer dashboard](https://console.developers.google.com/apis/dashboard) and create a project. 
- Once you have a project selected, you press `ENABLE APIS AND SERVICES` and turn on the Google Sheets API for your project.
- Go to the `OAuth consent screen` tab, and create an `Internal` project. If you want it to be external, you will have to wait for Google to verify your project. 
- Choose an application name and logo, then `Add scope -> ../auth/spreadsheets.readonly`. Click `Save`.
- Go to the `Credentials` tab and click `CREATE CREDENTIALS -> OAuth client ID`. Choose the Application type `Other`. 
- Fork this project and replace `client_id` and `client_secret` in `client_secret.json` with the credentials you just created.
- Build the docker image: `docker build -t gsheets2tboards .` 
- Run it! `docker run -it gsheets2tboards`