# Log Analysis

In this project, a large database with over a million rows is explored. And complex queries are written to draw business conclusions from data.

The database in the question is a newspaper website database where we have 3 tables: `articles`, `authors` and `log`.

* The `authors` table includes information about the authors of articles.
* The `articles` table includes the articles themselves.
* The `log` table includes one entry for each time a user has accessed the site.

### PreRequisites:
- Python3
- Vagrant
- VirtualBox

### Setup
1. Install Vagrant And VirtualBox
2. Download [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) from here. 
3. Unzip the file after downoading it.
4. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine
2. Clone this repository.

### To Run

1. Launch Vagrant VM by running `vagrant up`, you can the log in with `vagrant ssh`

2. To load the data, use the command `psql -d news -f newsdata.sql`.

3. Before running the python program, you need to create the pre-requisite postgreSQL database views which are used by the python code.
From the vagrant directory in your virtual box, run the following command to connect to the database

`psql -d news`

4. Create status_log and error_log views using the following commands :

`create view status_log as select time::timestamp::date as date,count(*) as status_count from log group by time::timestamp::date;`

`create view error_log as select time::timestamp::date as date,count(*) as error_count from log where status like '%4%' group by time::timestamp::date;`

5. To execute the program, run `python3 newsdatadb.py` from the command line.

