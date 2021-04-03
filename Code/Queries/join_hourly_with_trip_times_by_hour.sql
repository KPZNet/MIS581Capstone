
INSERT INTO public.hourlyriderstriptimes(date, hour, source, dest, riders, triptime, depart_date, depart_hour)

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

from hourlyriders, trips where
(trips.origin = hourlyriders.source AND trips.dest = hourlyriders.dest)

