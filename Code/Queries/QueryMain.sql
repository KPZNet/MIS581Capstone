
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
