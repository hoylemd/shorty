drop table if exists urls;
create table urls(
    hash varchar(64) primary key,
    full_url varchar(1025)
);
