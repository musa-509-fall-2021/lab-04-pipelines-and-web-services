/*
Load Process

Take the files that we've created and load them both into the database. You
should end up with two tables: addresses and geocoded_address_results
*/

drop table if exists addresses;
create table addresses (
    address_id     integer,
    street_address text,
    city           text,
    state          text,
    zip            text
);

copy ...;

drop table if exists geocoded_address_results;
create table geocoded_address_results (
    address_id      integer,
    input_address   text,
    match_status    text,
    match_type      text,
    matched_address text,
    lon_lat         text,
    tiger_line_id   integer,
    tiger_line_side text
);

copy ...;
