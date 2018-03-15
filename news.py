#!/usr/bin/env python3

import psycopg2

# query 1: What are the three most popular articles of all time?
request_articles = """select articles.title, count(*) as num
            from articles,log
            where log.status='200 OK'
            and articles.slug = substr(log.path, 10)
            group by articles.title
            order by num desc
            limit 3;"""

# query 2: Who are the most popular article authors of all time?
request_authors = """select authors.name, count(*) as num
            from authors ,articles , log
            where log.status='200 OK'
            and authors.id = articles.author
            and articles.slug = substr(log.path, 10)
            group by authors.name
            order by num desc;
            """

# query 3: On which day did more than 1% of requests lead to errors?
request_errors = """select time, per_failed
            from percentagecount
            where per_failed > 1;
            """


# Query data from the database, open and close the connection
def query_db(sql_request):
    conn = psycopg2.connect(database="news")
    cursor = conn.cursor()
    cursor.execute(sql_request)
    results = cursor.fetchall()
    conn.close()
    return results


# Writing the report
# Print a title of the report
def print_title(title):
    print ("\n\t\t" + title + "\n")


# Print the top three articles of all time
def articles():
    articles = query_db(request_articles)
    print_title("Top 3 articles of all time")

    for title, num in articles:
        print(" \"{}\" -- {} views".format(title, num))


# Print the top authors of all time
def authors():
    authors = query_db(request_authors)
    print_title("Top authors of all time")

    for name, num in authors:
        print(" {} -- {} views".format(name, num))


# Print the days in which there were more than 1% bad requests
def most_error_days():
    most_error_days = query_db(request_errors)
    print_title("Days with more than one percentage of bad requests")

    for day, per_failed in most_error_days:
        print("""{0:%B %d, %Y}
            -- {1:.2f} % errors""".format(day, per_failed))


if __name__ == '__main__':
    articles()
    authors()
    most_error_days()
