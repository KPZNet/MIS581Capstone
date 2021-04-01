truncate routes;

INSERT INTO public."routes"(
	"origin", "dest", "name", "triptime", "mintriptime", "maxtriptime", "id")
select (origin),
       (dest ),
       (origin || ' - ' || dest)  as name,
       AVG(triptime), min(triptime), max(triptime),
       (origin || dest)  as id
        from triptimes group by dest, origin