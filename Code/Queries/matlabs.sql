-- Riders summed by source by day
select SUM(riders) as riders, depart_date, extract(ISODOW from depart_date)
from hourlystationqueue
where
        depart_hour = 8
  AND
        extract(ISODOW from depart_date) <= 5
  AND
        source = 'PITT'
  and extract(YEAR from depart_date) = 2014
group by depart_date
order by depart_date


select SUM(riders) as riders, extract(ISODOW from depart_date)
from hourlystationqueue
where
        depart_hour = 8
  AND
        extract(ISODOW from depart_date) <= 5
  AND
        source = 'PITT'
  and extract(YEAR from depart_date) = 2014
  and extract(MONTH from depart_date) in (3,4)
group by extract(ISODOW from depart_date)



select SUM(riders) as riders, depart_hour
from hourlystationqueue
where
        extract(ISODOW from depart_date) <= 5
  AND
        source = 'PITT'
  and extract(YEAR from depart_date) = 2014
group by depart_hour


select sum(riders), source, dest, extract(WEEK from depart_date) as week
from hourlystationqueue
where
        extract(ISODOW from depart_date) in (1,2,3,4,5)
  AND
        source = 'PITT'
  and
        depart_hour = 7
  and
        extract(YEAR from depart_date) in (2015)
group by source, dest, week
order by week ASC
