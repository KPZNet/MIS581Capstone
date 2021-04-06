-- Table: public.hourlystationqueue_clean

DROP TABLE IF EXISTS public.hourlystationqueue_clean CASCADE;

CREATE TABLE public.hourlystationqueue_clean
(
    date date,
    hour integer,
    source character varying COLLATE pg_catalog."default",
    dest character varying COLLATE pg_catalog."default",
    riders integer,
    triptime integer,
    depart_date date,
    depart_hour integer
)

    TABLESPACE pg_default;

ALTER TABLE public.hourlystationqueue_clean
    OWNER to postgres;

INSERT INTO hourlystationqueue_clean(date, hour, source, dest, riders,
                                     triptime, depart_date, depart_hour)
select * from hourlystationqueue where extract(YEAR from date) = 2015

