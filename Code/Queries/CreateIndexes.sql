create index on hourlystationqueue(date);
create index on hourlystationqueue(hour);
create index on hourlystationqueue(date, hour);
create index on hourlystationqueue(source);
create index on hourlystationqueue(dest);
create index on hourlystationqueue(source, dest);
create index on hourlystationqueue(depart_date);
create index on hourlystationqueue(depart_hour);
create index on hourlystationqueue(depart_date,depart_hour);

create index on bartstations(abbr);

create index on routelines(abbr);
create index on routelines(origin);
create index on routelines(dest);
create index on routelines(origin,dest);
create index on routelines(number);
create index on routelines(routeID);




