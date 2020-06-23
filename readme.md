This file manages server alerts(queues server side scripts to run).
Right now when website ARV gets a new insert it adds a record to alerts database
with the name of table that needs action, id of row in table, and action that needs to be taken.
