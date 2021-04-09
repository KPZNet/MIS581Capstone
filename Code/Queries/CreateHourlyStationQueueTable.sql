-- Table: public.hourlystationqueue

DROP TABLE IF EXISTS public.hourlystationqueue CASCADE;

CREATE TABLE public.hourlystationqueue
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

ALTER TABLE public.hourlystationqueue
    OWNER to postgres;


