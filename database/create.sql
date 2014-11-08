create table variable (
id int primary key,
name varchar(255),
min int, 
max int
);
create table function (
id int primary key,
type varchar(255)
);
create table term (
id int primary key,
value varchar(255),
function int references function(id),
points varchar(255)
);
create table variable_terms (
variable int references variable(id),
term int references term(id)
);
create table hedge (
id int primary key,
value varchar(255), 
result varchar(255)
);
create table variable_hedges (
variable int references variable(id),
hedge int references hedge(id)
);
