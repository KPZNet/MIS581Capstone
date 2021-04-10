create index on hourlystationqueue(date);
create index on hourlystationqueue(hour);
create index on hourlystationqueue(source);
create index on hourlystationqueue(dest);
create index on hourlystationqueue(depart_date);
create index on hourlystationqueue(depart_hour);

create index on hourlystationqueue(date, hour);
create index on hourlystationqueue(depart_hour, depart_date);
create index on hourlystationqueue(source, dest);