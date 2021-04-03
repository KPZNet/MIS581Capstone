with trips as
         (select origin,
                 dest,
                 AVG(triptime)
          from triptimes group by dest, origin)
select * from trips where origin = 'PITT' and dest = 'EMBR'