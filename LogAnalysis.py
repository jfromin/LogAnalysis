#!/usr/bin/env python3

import sys
import psycopg2
import re


# getData() function for creating a Postgresql connection, executing sql
# passed as parameter, fetching, closing, and returning results list.

def getData(sql):

    conn = psycopg2.connect("dbname=news")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# Retrive top 3 popular article by title, count.  Exclude 404 errors.
# Print with title formatted with double quotes.  Descending order
# by count.

def getPopularArticles():
    sql = 'SELECT A.TITLE, COUNT(B.STATUS) FROM ARTICLES A, LOG B'
    sql = sql + ' WHERE POSITION(\'/\' || lower(A.SLUG) IN lower(B.PATH)) > 0'
    sql = sql + ' AND B.STATUS <> \'404 NOT FOUND\''
    sql = sql + ' GROUP BY A.TITLE ORDER BY 2 DESC LIMIT 3;'
    # Retrive data from sql statement
    rows = getData(sql)
    for row in rows:
        print('"' + row[0] + '"' + u' \u2014 ' + str(row[1]) + " views")


# Print authors ordered by article popularity. Exclude 404 errors.

def getPopularAuthors():

    sql = 'SELECT A.NAME, COUNT (C.STATUS)'
    sql = sql + ' FROM AUTHORS A, ARTICLES B, LOG C'
    sql = sql + ' WHERE A.ID = B.AUTHOR'
    sql = sql + ' AND POSITION(\'/\' || lower(B.SLUG) IN lower(C.PATH)) > 0'
    sql = sql + ' AND C.STATUS <> \'404 NOT FOUND\''
    sql = sql + ' GROUP BY A.NAME ORDER BY 2 DESC;'
    # Retrive data from sql statement
    rows = getData(sql)
    for row in rows:
        print(row[0] + u' \u2014 ' + str(row[1]) + " views")


# Print all page requests where error percentage is greater
# than %1 on any given day.  Output date formatted as
# Month\sDay,\sYear.  Format decimal output as percentage.

def getErrorsByDay():

    sql = 'SELECT TO_CHAR(A.TIME,\'Month DD, YYYY\'), '
    sql = sql + 'ROUND(COUNT(C.STATUS)::NUMERIC/COUNT(A.STATUS)::NUMERIC,4)'
    sql = sql + ' FROM LOG A LEFT JOIN'
    sql = sql + '(SELECT * FROM LOG B WHERE B.STATUS IN (\'404 NOT FOUND\'))'
    sql = sql + ' AS C ON A.ID = C.ID'
    sql = sql + ' GROUP BY 1'
    sql = sql + ' HAVING ROUND(COUNT(C.STATUS)::NUMERIC'
    sql = sql + '/COUNT(A.STATUS)::NUMERIC,4) > .01'
    sql = sql + ' ORDER BY 2;'
    rows = getData(sql)
    rep = re.compile("\\s{2,}")
    for row in rows:
        print(rep.sub(' ', row[0])+u' \u2014 {:.1%}'.format(row[1])+" errors")


# Main driver.  handles cmd parameters one or all reports.
# displays help and syntax.

def main(argv):

    opts = ['--getpopulararticles', '--getpopularauthors', '--geterrorsbyday']
    opts.append('--all')

    # Is argument out of bounds?  try it!
    try:
        arg = argv[1].lower().replace(" ", "")
        if arg == opts[0]:
            getPopularArticles()
        elif arg == opts[1]:
            getPopularAuthors()
        elif arg == opts[2]:
            getErrorsByDay()
        elif arg == opts[3]:
            print("\nPopular Articles: ")
            getPopularArticles()
            print("\nPopular Authors: ")
            getPopularAuthors()
            print("\nErrors By Day: ")
            getErrorsByDay()
        elif arg == "--help" or arg not in opts:
            print('Syntax: LogAnalysis.py [' + '|'.join(map(str, opts)) + ']')
            print('Specify "LogAnalysis.py --help" to print this.')
    except (IndexError, ValueError):
        # If argument is out of bounds, display prompt.  clean exit.
        print('Specify "LogAnalysis.py --help" to print help.')
        sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
