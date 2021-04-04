
select count(*) from
(select count(*)
 from hourlyriders
group by source, dest) as foo



select count(*) from
    (select count(*)
     from triptimes
     group by origin, dest) as foo





    with trips as
         (select origin,
                 dest,
                 AVG(triptime) as triptime
          from triptimes group by dest, origin)

select *
from hourlyriders
         INNER JOIN trips ON
    (hourlyriders.source <> trips.origin AND hourlyriders.dest <> trips.dest)
