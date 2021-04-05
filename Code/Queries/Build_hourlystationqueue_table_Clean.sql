TRUNCATE hourlystationqueue_clean;

INSERT INTO hourlystationqueue_clean(date, hour, source, dest, riders,
                                     triptime, depart_date, depart_hour)
select * from hourlystationqueue where extract(YEAR from date) = 2015

