DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT USAGE ON SCHEMA public TO user1;

CREATE TABLE groups (
	id SERIAL PRIMARY KEY,
	is_variable BOOLEAN,
	is_term BOOLEAN,
	is_hedge BOOLEAN
);

CREATE TABLE synonims (
	id SERIAL PRIMARY KEY,
	group_id INT NOT NULL REFERENCES groups(id),
	lemma VARCHAR(255),
	grammemes VARCHAR(255),
	hits INT
);

CREATE TABLE variables (
	id SERIAL PRIMARY KEY,
	name_id INT NOT NULL REFERENCES groups(id),
	name VARCHAR(255),
	validated BOOLEAN,
	min REAL, 
	max REAL 
);

CREATE TABLE functions (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255)
);

CREATE TABLE terms (
	id SERIAL PRIMARY KEY,
	name_id INT NOT NULL REFERENCES groups(id),
	name VARCHAR(255),
	validated BOOLEAN,
	function_id INT NOT NULL REFERENCES functions(id),
	points VARCHAR(255)
);

CREATE TABLE variables_terms (
	variable_id INT NOT NULL REFERENCES variables(id) ON DELETE CASCADE,
	term_id INT NOT NULL REFERENCES terms(id) ON DELETE CASCADE
);

CREATE TABLE hedges (
	id SERIAL PRIMARY KEY,
	name_id INT NOT NULL REFERENCES groups(id),
	name VARCHAR(255),
	validated BOOLEAN,
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
	parent_id INT NULL REFERENCES nodes(id) ON DELETE CASCADE,
	type_id INT NOT NULL REFERENCES types(id),
	variable_id INT NULL REFERENCES variables(id) ON DELETE CASCADE,
	term_id INT NULL REFERENCES terms(id) ON DELETE CASCADE,
	hedge_id INT NULL REFERENCES hedges(id) ON DELETE CASCADE
);

CREATE TABLE closures (
	ancestor_id INT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
	descendant_id INT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
	PRIMARY KEY (ancestor_id, descendant_id)
);

CREATE TABLE rules (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255),
	validated BOOLEAN,
	antecedent_id INT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
	consequent_id INT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE
);

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO user1;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user1;

INSERT INTO functions (name) VALUES 
	('Z-функция'),
	('синглтон'),
	('треугольник'),
	('трапеция'),
	('S-функция');

INSERT INTO types (name) VALUES 
	('variable'),
	('hedge'),
	('term'),
	('term_complex'),
	('variable_value'),
	('term_and'),
	('term_or'),
	('variable_and'),
	('variable_or'),
	('variable_not');
