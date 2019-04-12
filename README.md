# LogAnalysis

Log Analysis is a simple reporting python reporting script that queries the "news" database and displays reports based on user input.

## Usage

LogAnalysis can be ran from the command line of referenced in the 'import' statement in another Python script.  
This script was built using Python 3.7.2. You should have Python 3 already installed. You can check the
version of Python installed by running the following from the command line:

```shell
python --version
```

To run LogAnalysis for all reports from cmd line:

```shell
python LogAnalysis.py --all
```

_To run LogAnalysis for individual reports, see Documentation section._

To print LogAnalysis help prompt (displays individual report options):

```shell
python LogAnalysis.py --help
```

Place the LogAnalysis.py file in the same directory as your Python script and put
the following statement at the top of your script:

```python
import LogAnalysis
```

## Documentation

As of 04/12/2019 there are three reports provided by the LogAnalysis script. Descriptions
of report below below:

-Get Popular Articles

Retrive top 3 popular article by title & count (page visits) and exclude 404 errors.
Output formatted with title wrapped in double quotes.  Results are in descending order by count.

```python
python LogAnalysis.py --getpopulararticles
```

e.g. "Man Bites Dog...Again!" — 2839382 views

-Get Popular Authors

Print authors ordered by article popularity (page visits) and exclude 404 errors.

```python
python LogAnalysis.py --getpopularauthors
```

e.g. Barry Johnson — 28192 views

-Get Errors by Day

Retrive all page requests where error percentage is greater than %1 on any given day.
Output date formatted as Month Day, Year and decimal output as percentage.

```python
python LogAnalysis.py --geterrorsbyday
```

e.g. July 10, 2011 — 5.3% errors

## Supported versions

Python 3.7.2 is the only version that this script was tested.  Older/Newer versions may work also.