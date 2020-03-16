CREATE TABLE demo.netflix_master (
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