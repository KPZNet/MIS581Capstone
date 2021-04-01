with trips as
(select hour, (origin),
       (dest ),
       (origin || ' - ' || dest)  as name,
       AVG(triptime), min(triptime), max(triptime),
       (origin || dest)  as id
        from triptimes group by dest, origin, hour)
select *, to_char(hourlyriders.date, 'Day') AS "DayName"
from hourlyriders, trips where
EXTRACT(YEAR from hourlyriders.date) = 2018
and
hourlyriders.dest = 'EMBR'
and
EXTRACT(DOW from hourlyriders.date) = 1
and
hourlyriders.hour = 8
and hourlyriders.hour = trips.hour
and hourlyriders.source = trips.origin
AND hourlyriders.dest = trips.dest