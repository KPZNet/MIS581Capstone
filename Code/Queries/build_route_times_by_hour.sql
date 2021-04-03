select hour, (origin),
       (dest ),
       (origin || ' - ' || dest)  as name,
       AVG(triptime), min(triptime), max(triptime),
       max(triptime) - min(triptime) as spread,
       ((max(triptime) - min(triptime))/AVG(triptime))*100 as percentdiff,
       (origin || dest)  as id
        from triptimes group by dest, origin, hour