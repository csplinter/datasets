# Netflix Dataset

Contains data from all Netflix titles and movies as of 2019

Source: https://www.kaggle.com/shivamb/netflix-shows

License: [Creative Commons: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)

[](#dd-001)
## Cassandra Tutorial

### Create database schema 

In a CQL Shell execute the following
```
CREATE KEYSPACE IF NOT EXISTS demo WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS demo.netflix_master (
    show_id int,
    cast list<text>,
    country list<text>,
    date_added date,
    description text,
    director list<text>,
    duration text,
    listed_in list<text>,
    rating text,
    release_year int,
    title text,
    type text,
    PRIMARY KEY ((title), show_id)
);

CREATE TABLE IF NOT EXISTS demo.netflix_titles_by_date (
    show_id int,
    date_added date,
    release_year int,
    title text,
    PRIMARY KEY ((release_year), date_added, show_id))
WITH CLUSTERING ORDER BY (date_added DESC);


CREATE TABLE IF NOT EXISTS demo.netflix_titles_by_rating (
    show_id int,
    rating text,
    title text,
    PRIMARY KEY ((rating), show_id)
);
```
[](#dd-002)
### Load data 

Load data into `demo.netflix_master`
```
dsbulk load -k demo -t netflix_master -url netflixdata-clean.csv --codec.date "MMMM d, y"
```

Load data into `demo.netflix_titles_by_date`
```
dsbulk load -k demo -t netflix_titles_by_date -url netflixdata-clean.csv --codec.date "MMMM d, y" -m "show_id,title,release_year,date_added"
```

Load data into `demo.netflix_titles_by_rating`
```
dsbulk load -k demo -t netflix_titles_by_rating -url netflixdata-clean.csv --codec.date "MMMM d, y" -m "show_id,title,rating"
```
[](#dd-003)
### Read data

Get all data from netflix_master
```
select * from demo.netflix_master;
```

Get data from netflix_master by title
```
select * from demo.netflix_master where title = 'Pulp Fiction';
```

Get director from netflix_master by title
```
select director from demo.netflix_master where title = 'Pulp Fiction';
```

Get all titles released in 2019
```
select title from demo.netflix_titles_by_date where release_year = 2019;
```

Get all titles released in 2019 after June
```
select title from demo.netflix_titles_by_date where release_year = 2019 and date_added > '2019-06-01';
```

Get all titles rated G or TV-Y
```
select title from demo.netflix_titles_by_rating where rating IN ('G', 'TV-Y');
```

[](#dd-004)
### Write new data

```
insert into demo.netflix_master (title, show_id, cast, country, date_added, description, director, duration, listed_in, rating, release_year, type) values ('New show', 90000000, ['Tom Hardy'], ['United States'], '2020-04-12', 'Experiences of an awesome developer', ['Francis Ford Coppola'], '1 Season', ['Drama'], 'TV-14', 2020, 'TV Show');
```
```
insert into demo.netflix_titles_by_date (title, show_id, release_year, date_added) values ('New show', 90000000, 2020, '2020-04-12');
```
```
insert into demo.netflix_titles_by_rating (title, show_id, rating) values ('New show', 90000000, 'TV-14');
```

[](#dd-005)
### Update existing data

```
update demo.netflix_master set duration = '4 Seasons' where title = 'La casa de papel' and show_id = 80192098;
```
