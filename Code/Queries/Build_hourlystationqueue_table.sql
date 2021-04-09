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

INSERT INTO public.hourlystationqueue(date, hour, source, dest, riders,
                                         triptime, depart_date, depart_hour)

with trips as
(select origin,
        dest,
        AVG(triptime) as triptime
from triptimes group by dest, origin)

select hourlyriders.date, hourlyriders.hour, hourlyriders.source, hourlyriders.dest, hourlyriders.riders,
       trips.triptime,

       CASE
           WHEN trips.triptime >= 60 AND hourlyriders.hour = 0
               THEN  cast(hourlyriders.date - interval '1' DAY as Date)
          ELSE
               cast(hourlyriders.date as Date)

           END depart_date,

CASE
           WHEN trips.triptime >= 60 AND hourlyriders.hour = 0
                THEN  23
           WHEN trips.triptime >= 60 AND hourlyriders.hour >0
                THEN hourlyriders.hour - 1
           ELSE hourlyriders.hour

END depart_hour

from hourlyriders
INNER JOIN trips ON
(hourlyriders.source = trips.origin AND hourlyriders.dest = trips.dest)

