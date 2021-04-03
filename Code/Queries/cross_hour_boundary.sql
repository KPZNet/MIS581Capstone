with trips as
         (select hour, origin, dest ,
                 (origin || ' - ' || dest)  as name,
                 AVG(triptime) as AVG, min(triptime) as MIN, max(triptime) as MAX,
                 (origin || dest)  as id
          from triptimes group by dest, origin, hour)
select hourlyriders.source, hourlyriders.dest,
       trips.MIN, trips.MAX,
       to_char(hourlyriders.date, 'Day') AS "DayName"
from hourlyriders, trips where
        trips.MIN < 60 and trips.MAX > 60
and
    hourlyriders.hour = 8
       and hourlyriders.hour = trips.hour
       and hourlyriders.source = trips.origin
       AND hourlyriders.dest = trips.dest