-- Table: public.hourlyriderstriptimes

-- DROP TABLE public.hourlyriderstriptimes;

CREATE TABLE public.hourlyriderstriptimes
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

ALTER TABLE public.hourlyriderstriptimes
    OWNER to postgres;


