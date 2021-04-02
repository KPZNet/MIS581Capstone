
-- Remove all tables to start with clean slate

DROP TABLE IF EXISTS public."routelines" CASCADE;

CREATE TABLE public.routelines
(
    name character varying COLLATE pg_catalog."default",
    number integer,
    origin character(4)[] COLLATE pg_catalog."default",
    dest character(4)[] COLLATE pg_catalog."default",
    id serial primary key
);

TRUNCATE routelines RESTART IDENTITY;


COPY public.routelines(name, number, origin, dest)
FROM '/Users/KenCeglia/Documents/MIS581Capstone/Code/Queries/bart_lines.csv'
DELIMITER ',' ;
CSV HEADER;

-- Row Output per Table

SELECT *
FROM public."routelines"
LIMIT 10;


 


