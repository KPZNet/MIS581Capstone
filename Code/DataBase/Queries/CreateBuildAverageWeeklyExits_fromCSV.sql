-- Table: public.bartyearlyexits

DROP TABLE IF EXISTS public.bartyearlyexits CASCADE;

CREATE TABLE public.bartyearlyexits
(
    station character varying COLLATE pg_catalog."default",
    abbr character varying COLLATE pg_catalog."default",
    year integer,
    riders integer
)

    TABLESPACE pg_default;

ALTER TABLE public.bartyearlyexits
    OWNER to postgres;

TRUNCATE bartyearlyexits RESTART IDENTITY;

COPY public.bartyearlyexits(station, abbr, year, riders)
    FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/AverageWeekdayExits.csv'
    DELIMITER ','
CSV HEADER;

-- Row Output per Table

SELECT *
FROM public.bartyearlyexits
LIMIT 10;

