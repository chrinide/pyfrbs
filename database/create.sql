DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT USAGE ON SCHEMA public TO user1;
CREATE TABLE variable (
	id INT PRIMARY KEY,
	name VARCHAR(255),
	min REAL, 
	max REAL 
);
CREATE TABLE function (
	id INT PRIMARY KEY,
	type VARCHAR(255)
);
CREATE TABLE term (
	id INT PRIMARY KEY,
	value VARCHAR(255),
	function_id INT NOT NULL REFERENCES function(id),
	points VARCHAR(255)
);
CREATE TABLE variable_term (
	variable_id INT NOT NULL REFERENCES variable(id),
	term_id INT NOT NULL REFERENCES term(id)
);
CREATE TABLE hedge (
	id INT PRIMARY KEY,
	value VARCHAR(255),
	result VARCHAR(255)
);
CREATE TABLE variable_hedge (
	variable_id INT NOT NULL REFERENCES variable(id),
	hedge_id INT NOT NULL REFERENCES hedge(id)
);
CREATE TABLE type (
	id INT PRIMARY KEY,
	name VARCHAR(255)
);
CREATE TABLE node (
	id INT PRIMARY KEY,
	type_id INT NOT NULL REFERENCES type(id),
	variable_id INT,
	term_id INT,
	hedge_id INT
);
CREATE TABLE closure (
	ancestor_id INT NOT NULL REFERENCES node(id),
	descendant_id INT NOT NULL REFERENCES node(id),
	PRIMARY KEY (ancestor_id, descendant_id)
);
CREATE TABLE rule (
	id INT PRIMARY KEY,
	antecedent_id INT NOT NULL REFERENCES node(id),
	consequent_id INT NOT NULL REFERENCES node(id)
);
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO user1;
