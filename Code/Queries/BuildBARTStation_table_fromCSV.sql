-- Table: public.bartstations

DROP TABLE IF EXISTS public.bartstations CASCADE;

CREATE TABLE public.bartstations
(
    name character varying COLLATE pg_catalog."default",
    abbr character varying COLLATE pg_catalog."default",
    gtfslat character varying COLLATE pg_catalog."default",
    gtfslong character varying COLLATE pg_catalog."default",
    city character varying COLLATE pg_catalog."default",
    id integer
)

    TABLESPACE pg_default;

ALTER TABLE public.bartstations
    OWNER to postgres;

TRUNCATE bartstations RESTART IDENTITY;

COPY public.bartstations(name, abbr, gtfslat, gtfslong, city, id)
    FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/all_stations.csv'
    DELIMITER ','
CSV HEADER;

-- Row Output per Table

SELECT *
FROM public.bartstations
LIMIT 10;

