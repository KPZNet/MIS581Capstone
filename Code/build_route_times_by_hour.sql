select hour, (origin),
       (dest ),
       (origin || ' - ' || dest)  as name,
       AVG(triptime), min(triptime), max(triptime),
       (origin || dest)  as id
        from triptimes group by dest, origin, hour