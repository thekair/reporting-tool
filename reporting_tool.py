#!/usr/bin/env python2.7
#
# This is a reporting tool that builds an informative summary from logs

import psycopg2

DBNAME = "news"


def get_reports():
    """Return all reports from the database"""
    print "START OF REPORT"
    print ""
    get_popular_articles()
    print ""
    get_popular_authors()
    print ""
    get_failure_rate()
    print ""
    print "END OF REPORT"


def get_popular_articles():
    """Return most popular three articles, most popular first."""
    print "--Top_Three_Popular_Articles--"
    query = "select article_title, views from author_views limit 3"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    for i, row in c:
        print i, "--", row, "views"
    db.close()


def get_popular_authors():
    """Return all authors, most popular first."""
    print "--Most_Popular_Authors--"
    query = "select author_name,total_views from popular_author"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    for i, row in c:
        print i, "--", row, "views"
    db.close()


def get_failure_rate():
    """return dates in which more than 1% of requests lead to errors"""
    print "--Warning_Watch--"
    query = "Select to_char(date, 'Mon DD, YYYY'), failure_percentage " \
            "from failure_rate where failure_percentage > 1.00"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    for i, row in c:
        print i, "--", row, "% errors"
    db.close()

get_reports()
