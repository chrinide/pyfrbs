DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT USAGE ON SCHEMA public TO user1;
CREATE TABLE variables (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255),
	min REAL, 
	max REAL 
);
CREATE TABLE functions (
	id SERIAL PRIMARY KEY,
	type VARCHAR(255)
);
CREATE TABLE terms (
	id SERIAL PRIMARY KEY,
	value VARCHAR(255),
	function_id INT NOT NULL REFERENCES functions(id),
	points VARCHAR(255)
);
CREATE TABLE variables_terms (
	variable_id INT NOT NULL REFERENCES variables(id) ON DELETE CASCADE,
	term_id INT NOT NULL REFERENCES terms(id) ON DELETE CASCADE
);
CREATE TABLE hedges (
	id SERIAL PRIMARY KEY,
	value VARCHAR(255),
	result VARCHAR(255)
);
CREATE TABLE variables_hedges (
	variable_id INT NOT NULL REFERENCES variables(id) ON DELETE CASCADE,
	hedge_id INT NOT NULL REFERENCES hedges(id) ON DELETE CASCADE
);
CREATE TABLE types (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255)
);
CREATE TABLE nodes (
	id SERIAL PRIMARY KEY,
	parent_id INT NOT NULL REFERENCES nodes(id),
	type_id INT NOT NULL REFERENCES types(id),
	variable_id INT,
	term_id INT,
	hedge_id INT
);
CREATE TABLE closures (
	ancestor_id INT NOT NULL REFERENCES nodes(id),
	descendant_id INT NOT NULL REFERENCES nodes(id),
	PRIMARY KEY (ancestor_id, descendant_id)
);
CREATE TABLE rules (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255),
	antecedent_id INT NOT NULL REFERENCES nodes(id),
	consequent_id INT NOT NULL REFERENCES nodes(id)
);
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO user1;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user1;
