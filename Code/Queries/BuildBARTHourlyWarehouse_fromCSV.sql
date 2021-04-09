
-- Remove all tables to start with clean slate

DROP TABLE IF EXISTS public."hourlyriders" CASCADE;

-- Table: public.HourlyRiders

CREATE TABLE public."hourlyriders" (
        date date, hour integer, 
        source character varying COLLATE pg_catalog."default",
        dest character varying COLLATE pg_catalog."default",
        riders integer, id serial primary key);

TRUNCATE hourlyriders RESTART IDENTITY;



COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2021.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2020.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2019.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2018.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2017.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2016.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2015.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2014.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2013.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2012.csv'
DELIMITER ',' ;

COPY public.hourlyriders(date, hour, source, dest, riders)
FROM '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/date-hour-soo-dest-2011.csv'
DELIMITER ',' ;



-- Row Output per Table

SELECT *
FROM public."hourlyriders"
LIMIT 10;


 


