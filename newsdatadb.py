import psycopg2

DB_NAME = "news"

question1 = 'What are the most popular three articles of all time?'
query1 = """
        select title, count(*) as views
        from articles left join log
        on concat('/article/',articles.slug) = log.path
        where log.status like '%2%'
        group by log.path,articles.title
        order by views desc limit 3;"""


question2 = 'Who are the most popular article authors of all time?'
query2 = """
        select authors.name, count(*) as views
        from articles left join authors
        on articles.author = authors.id
        left join log
        on concat('/article/',articles.slug) = log.path
        where log.status like '%2%'
        group by authors.name
        order by views desc;"""

question3 = 'On which days did more than 1% of requests lead to errors?'
query3 = """
        select status_log.date,
        round(cast((100*error_count) as numeric) /
        cast(status_count as numeric), 2)
        as error
        from status_log join error_log
        on status_log.date=
        error_log.date
        where ((error_count * 100)/status_count::float) > 1;"""


def connect():
    db = psycopg2.connect(database=DB_NAME)
    cursor = db.cursor()
    return db, cursor


def get_query_results(query):
    db, cursor = connect()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def print_query_results(question, query_results):
    print('')
    print(question)
    for result in query_results:
        print ('\t' + str(result[0]) + '   -  ' + str(result[1]) + ' views')


def print_query_errorday_results(question, query_results):
    print('')
    print(question)
    for result in query_results:
        print ('\t' + str(result[0]) + '   -  ' + str(result[1]) + '%')


if __name__ == '__main__':

    most_popular_articles_results = get_query_results(query1)
    most_popular_authors_results = get_query_results(query2)
    error_days = get_query_results(query3)

    print_query_results(question1, most_popular_articles_results)
    print_query_results(question2, most_popular_authors_results)
    print_query_errorday_results(question3, error_days)
