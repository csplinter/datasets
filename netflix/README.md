# Netflix Dataset

Contains data from all Netflix titles and movies as of 2019

Source: https://www.kaggle.com/shivamb/netflix-shows

License: [Creative Commons: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)

## Cassandra Tutorial

### Create database schema 

In a CQLSH shell execute the following
```
CREATE TABLE demo.netflix_master (
    show_id int PRIMARY KEY,
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
    type text
);

CREATE TABLE demo.netflix_titles_by_date (
    show_id int,
    date_added date,
    release_year int,
    title text,
    PRIMARY KEY ((release_year), date_added, show_id))
WITH CLUSTERING ORDER BY (date_added DESC);

CREATE TABLE demo.netflix_titles_by_rating (
    show_id int,
    rating text,
    title text,
    PRIMARY KEY ((rating), show_id)
);
```

### Load data 

Load data into `demo.netflix_master`
```
dsbulk load -k demo -t netflix_master -url netflixdata-clean.csv --codec.date "MMMM d, y"
```

Load data into `demo.netflix_titles_by_date`
```
dsbulk load -k demo -t netflix_titles_by_date -url netflixclean.csv --codec.date "MMMM d, y" -m "show_id,title,release_year,date_added"
```

Load data into `demo.netflix_titles_by_rating`
```
dsbulk load -k demo -t netflix_titles_by_rating -url netflixclean.csv --codec.date "MMMM d, y" -m "show_id,title,rating"
```

### Query data

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
select title from demo.netflix_titles_by_date where release_year = '2019';
```

Get all titles released before 2017
```
select title from demo.netflix_titles_by_date where release_year < '2017';
```

Get all titles rated G or TV-Y
```
select title from demo.netflix_titles_by_rating where rating IN ('G', 'TV-Y');
```