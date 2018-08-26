# Reporting tool

 A reporting tool that builds an informative summary from logs stored in a database.

### Program Design

This is a server-side Python code that resides in the sourcefile `reporting_tool.py` in which it connects to a local database running `PostgreSQL`. The python code uses the `psycopg2` Python module to connect to the DB.

The code runs a master function to generate the report called `get_reports()`
The code has three sub functions in which each function is used by `get_reports()` to answer a spesific question by querying the database.


## Getting Started

Please follow the below steps in order to generate the report

### 1- Setup the virtual machine

* Open a Unix-style terminal on your computer.
* Install [VirtualBox](https://www.virtualbox.org/) to run a virtual machine.
* Install [Vagrant](https://www.vagrantup.com/downloads.html) which will configure the VM and lets you share files between your host computer and the VM's filesystem.
* Download the VM configuration by downloading and unziping this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called `FSND-Virtual-Machine`. It may be located inside your Downloads folder.
* Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.
* Start the virtual machine - From your terminal, inside the vagrant subdirectory, run the command `vagrant up`
* Run `vagrant ssh` to log in to your newly installed Linux VM!


### 2- Download the data

* Download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) - You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
* Inside the VM, change directory to vagrant by running `cd /vagrant`
* Load the site's data into your local database - From the vagrant directory and use the command `psql -d news -f newsdata.sql`

### 3- Create views in the Database

The code relies on the following database views so make sure you create the views before running the program.

*  connect to the database -- from the terminal cd to vagrant directory then run `psql -d news`.

* Create a view to show number of successful views per page:
`create view article_views as 
select REPLACE (path, '/article/', '') as article, count(id) as views 
from log where status = '200 OK' and path!='/' 
group by path 
order by views desc;`

* Create a view to show number of views per article “linked with author name”:

`create view author_views as 
select s.name as author_name, r.title as article_title, v.views 
from article_views as v, articles r, authors s 
where v.article=r.slug and r.author=s.id
order by v.views desc;`

* Create a view to show most popular author:

`create view popular_author as 
select author_name, sum(views) as total_views 
from author_views 
group by author_name 
order by total_views desc;`

* Create a view to show list of error rate per date

`create view failure_rate as
select a.date, a.success_count, b. failure_count, cast(cast(b. failure_count as float)/a.success_count *100 as decimal(18,1)) as failure_percentage
from
(select time::timestamp::date as date, count(id) as success_count from log where status = '200 OK' group by date) as A,
(select time::timestamp::date as date, count(id) as failure_count from log where status != '200 OK' group by date) as B
where a.date = b.date
order by a.date;`


### 4- Generate the report
* Download source file reporting_tool.py into the vagrant directory in your computer.
* From the `terminal` cd into vagrant directory then run the program using the command `python reporting_tool.py`.



## Built With

* [Python](http://www.python.org/) - The development language
* [PostgreSQL](https://www.postgresql.org/) - The relational database system

## License

This project is open source
