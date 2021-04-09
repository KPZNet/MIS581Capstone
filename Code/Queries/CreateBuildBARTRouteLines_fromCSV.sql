
-- Remove all tables to start with clean slate

DROP TABLE IF EXISTS public."routelines" CASCADE;

CREATE TABLE public.routelines
(
    abbr character varying COLLATE pg_catalog."default",
    routeID character varying COLLATE pg_catalog."default",
    origin character(4)[] COLLATE pg_catalog."default",
    dest character(4)[] COLLATE pg_catalog."default",
    number integer,
    station character varying COLLATE pg_catalog."default"
);

TRUNCATE routelines RESTART IDENTITY;


COPY public.routelines(name, number, origin, dest)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/all_bart_lines.csv'
DELIMITER ','
CSV HEADER;

-- Row Output per Table

SELECT *
FROM public."routelines"
LIMIT 10;


 


