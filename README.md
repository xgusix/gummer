#Gummer
## What is Gummer?

Gummer is a framework for hunting malware. It is based on anomalies and it is 
written in python.

The name of this framework comes from a very famous *gravoid* hunter called Burt
Gummer, who appears in all the *Tremors* movies.

![BurtGummer.jpg](https://raw.githubusercontent.com/xgusix/gummer/master/doc/BurtGummer.jpg)

Also, this: [gummer](http://www.urbandictionary.com/define.php?term=gummer) @ 
urbandictionary.com

Gummer is basically a database query engine. It provides an easy way to have 
your list of anomalies connected to your different databases, returning the
results in different formats.

Gummer was mainly created with the purpose of reducing the detection time of the
increasing number of the so-called APTs. It also happens to be very helpful for
Incident Response tasks, when trying to contain an incident and not knowing
where to start the analysis.

It’s important to highlight that using Gummer as an IDS is not recommended if
you are not specifically looking for this kind of threat. This is because the s
earch of anomalies, or “weak signals”, can lead to a high number of false 
positives, which will result in people spending time reviewing the alerts.

Gummer is executed from the command line, it is multiplatform and it's in a
beta stage.

## Using Gummer

When we want to spot a specific anomaly, we run Gummer from the CLI, as follows:
```
python gummer.py –a <analyzer_id> -db <db_connector_id> -o <output_id>
```
In the above command, we are passing the arguments of the different modules that
Gummer will use during its execution.

## Gummer options:
```
$ python gummer.py -h
usage: gummer.py [-h] [-l] [-ldb] [-lo] [-lc] [-a ANALYZER] [-db DBCONNECTOR]
                 [-o OUTPUT] [-c COLLECTOR]

optional arguments:
  -h, --help            show this help message and exit
  -l, --list_anal       List analyzers.
  -ldb, --list_databases
                        List db connectors.
  -lo, --list_outputs   List possible output formats.
  -lc, --list_collectors
                        List collectors.
  -a ANALYZER, --analyzer ANALYZER
                        ID of the analyzer to use.
  -db DBCONNECTOR, --dbconnector DBCONNECTOR
                        ID of the database connector to use.
  -o OUTPUT, --output OUTPUT
                        ID of the output to use.
  -c COLLECTOR, --collector COLLECTOR
                        ID of the collector to use.
```
# The framework

This framework is based on a working instance of a similar product that I worked
with in the past. The product proved to work well, so I decided to write my own
version of it, making it easier to adapt to different environments.

In order to make it flexible, the framework is based on different modules: there
is the main executable, gummer.py, which is supported by some other auxiliary
functions, and there are the modules of the framework.

![Gummer FW.png](https://raw.githubusercontent.com/xgusix/gummer/master/doc/modules.png)

#Modules

The modules are small snippets of code that are imported on demand by
*gummer.py*. They perform different tasks and are connected by *gummer.py* to
perform the search of the anomalies on any of our databases and do whatever we
want with the output.

There are four kinds of modules: Collectors, Outputs, Analyzers and Database
connectors

## Collectors

The first thing we need to do when working with Gummer is to feed data to it.
To do that, we use the collectors.

A collector is a parser that processes the logs and inserts them into a database.
To start a collection process you must execute the following command:

```
python gummer.py –c <collector_id> -db <db_connector_id> -o <output_id>
```
The general structure of a collector is the following:

```python
import db_loader

aid = "unique_id"
name = "name of the collector"
desc = "Description of the collector"

def launch(connector):
    """
    Parselog and DB insertion
    query = "insert..."
    data = db_loader.db_query(connector, query)
    """
    return suc, fail #Returns de number of successful and failed insertions.
```

We need to import *db_loader* to be able to connect to the database from which
we are going to get the data. That is also the reason why the function *launch*
receives "connector". "connector" is the module that connects to the database
from which the analyzer is going to retrieve the information.

Usually (and up until now I haven’t found a different way to do this), when I
want to parse a log file I process it and insert the entries one by one in the
database. To do this, I use a loop where I keep count of the successful and
failed insertions. This count is what needs to be returned at the end of the
collection.

This count is only useful for debugging and logging purposes, so you can just
parse the log, insert the different lines in the database and then
"return 0, 0".

## Outputs

The output modules perform the actions needed in order to return the data in
the desired format. What does that mean? Basically, you can do whatever you
want/can with the output.

The output module receives data and processes it in any way you want. The
supplied examples are designed to print in the CLI, but you can write connectors
 to SIEMs, send the results via e-mail... mostly anything you want.

The basic structure of an output module is the following:

```python
aid = "unique_id"
name = "name of the output"
desc = "Description of the output"

def launch(data):
    """Process data"""
```
If you launch a command without specifying any output, it will use the default
output. The default output is define in the global variable “DEFAULT_OUTPUT” in
*gummer.py*.

## Analyzers

Analyzers are the core of Gummer. You must have in mind that all the value of
this framework is in the anomalies that you define within the analyzers.

Gummer queries databases to search for the data needed to define the different
anomalies. The data retuned by these anomalies is normally going to be the
result of a query, but the functionality of the analyzers is only limited by
your knowledge of python.

Executing an analyzer:

```
python gummer.py –a <analyzer_id> -db <db_connector_id> -o <output_id>
```


The structure of an analyzer is the following:

```python
import db_loader

aid = "unique_id"
name = "name of the analyzer"
desc = "Description of the analyzer"

def launch(connector):
    """Definition of the analyzer"""
    query = "select * from db"
    data = db_loader.db_query(connector, query)
    return data
```

We need to import *db_loader* to be able to connect to the database from which
we are going to get the data. That is also the reason why the function *launch*
receives "connector". "connector" is the module that connects to the database
from which the analyzer is going to retrieve the information.

The result of the query is stored in the variable data and it is returned to
*gummer.py* in order to be passed to the selected output module. Therefore,
it’s very important that the data type stored in the variable returned by the
analyzers is compatible with the selected output module.

## DB Connectors

The DB connectors are the modules that allow the other modules to connect to the
different databases.

These modules have to be very flexible and execute any query they receive. Thus,
their function is basically: to open a connection with the DB, execute a query,
close the connection, and return the information retrieved. You can find some
examples of the code in the folder *db_connectors*.

# Publishing Anomalies/Analyzers.

There are only three anomalies published with the framework under the path: 
analyzers/APT_book. These anomalies were published by the Dr. Eric Cole in the
book [Advanced Persistence Threat](http://www.bookdepository.com/Advanced-Persistent-Threat-Eric-Cole/9781597499491).

There are two main reasons why I won't publicly share more anomalies. The first
one is because if all these "rules" for hunting are made public, malware authors
can learn how to avoid them, which makes detection even harder. The second one
has to do with the NDAs that I have signed with the companies I’ve worked for.

I am definitely not against sharing this kind of knowledge. I just don't like
the idea of publishing it for everyone to see. There are communities, trusted
circles, where people exchange Yara rules, IoCs, etc. among the trusted people
who are part of those groups. If you want to create a community to share
analyzers, I'll be very happy to join you and support it, but I really just
refuse to share anomalies in the public repo.
