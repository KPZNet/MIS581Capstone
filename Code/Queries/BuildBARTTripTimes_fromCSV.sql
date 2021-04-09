
-- Remove all tables to start with clean slate

DROP TABLE IF EXISTS public."triptimes" CASCADE;

-- Table: public.triptimes

CREATE TABLE public.triptimes
(
    origin character varying COLLATE pg_catalog."default",
    dest character varying COLLATE pg_catalog."default",
    triptime integer,
    hour integer,
    origtimemin time without time zone,
    origtimedate date,
    desttimemin time without time zone,
    desttimedate date,
    dow integer,
    day character varying COLLATE pg_catalog."default",
    fare money,
    id serial primary key
);

TRUNCATE triptimes RESTART IDENTITY;

COPY public.triptimes(origin, dest, triptime, hour, 
origtimemin, origtimedate, desttimemin, desttimedate, dow, day, fare)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/route_trip_times 3-38 to 3-29 Line 1 .csv'
DELIMITER ',' 
CSV HEADER;


-- Row Output per Table

SELECT *
FROM public."triptimes"
LIMIT 10;





 


