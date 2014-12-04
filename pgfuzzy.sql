DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT USAGE ON SCHEMA public TO user1;

CREATE TABLE synonims (
	id SERIAL PRIMARY KEY,
	group_id INT NOT NULL,
	lemma VARCHAR(255),
	grammemes VARCHAR(255),
	hits INT,
	is_variable BOOLEAN,
	is_term BOOLEAN,
	is_hedge BOOLEAN
);

CREATE TABLE variables (
	id SERIAL PRIMARY KEY,
	name_id INT NOT NULL,
	min REAL, 
	max REAL 
);

CREATE TABLE functions (
	id SERIAL PRIMARY KEY,
	type VARCHAR(255)
);

CREATE TABLE terms (
	id SERIAL PRIMARY KEY,
	name_id INT NOT NULL,
	function_id INT NOT NULL REFERENCES functions(id),
	points VARCHAR(255)
);

CREATE TABLE variables_terms (
	variable_id INT NOT NULL REFERENCES variables(id) ON DELETE CASCADE,
	term_id INT NOT NULL REFERENCES terms(id) ON DELETE CASCADE
);

CREATE TABLE hedges (
	id SERIAL PRIMARY KEY,
	name_id INT NOT NULL,
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

INSERT INTO synonims (group_id, lemma, grammemes, hits, is_variable, is_term, is_hedge) VALUES
	(1, 'возраст', 'сущ еч', 1, true, false, false),
	(1, 'годы', 'сущ мч', 1, true, false, false),
	(2, 'время', 'сущ еч', 1, true, false, false),
	(2, 'часы', 'сущ мч', 1, true, false, false),
	(3, 'активность', 'сущ еч', 1, true, false, false),
	(4, 'молодой', 'прил', 1, false, true, false),
	(4, 'юный', 'прил', 1, false, true, false),
	(5, 'поздний', 'прил', 1, false, true, false),
	(6, 'низкий', 'прил', 1, false, true, false),
	(7, 'не', 'част', 1, false, false, true);

INSERT INTO variables (name_id, min, max) VALUES 
	(1, 0, 100),
	(2, 0, 24),
	(3, 0, 10);

INSERT INTO functions (type) VALUES 
	('трапеция');

INSERT INTO terms (name_id, function_id, points) VALUES 
	(4, 1, '15;20;25;30'),
	(5, 1, '0;1;3;4'),
	(6, 1, '0;1;2;3');

INSERT INTO variables_terms (variable_id, term_id) VALUES
	(1, 1),
	(2, 2),
	(3, 3);

INSERT INTO hedges (name_id, result) VALUES 
	(7, '1 - x');

INSERT INTO variables_hedges (variable_id, hedge_id) VALUES 
	(1, 1);

INSERT INTO types (name) VALUES 
	('term'),
	('hedge'),
	('variable'),
	('term_complex'),
	('variable_value'),
	('term_and'),
	('term_or'),
	('variable_and'),
	('variable_or'),
	('variable_not');

INSERT INTO nodes (id, parent_id, type_id, variable_id, term_id, hedge_id) VALUES
	(1, 1, 8, 0, 0, 0), (2, 1, 5, 0, 0, 0), (3, 2, 3, 1, 0, 0), 
	(4, 2, 4, 0, 0, 0), (5, 4, 2, 0, 0, 1), (6, 4, 1, 0, 1, 0), 
	(7, 1, 5, 0, 0, 0), (8, 7, 3, 2, 0, 0), (9, 7, 1, 0, 2, 0), 
	(10, 10, 5, 0, 0, 0), (11, 10, 3, 3, 0, 0), (12, 10, 1, 0, 3, 0);

INSERT INTO closures (ancestor_id, descendant_id) VALUES
	(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
	(1, 8), (1, 9), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
	(3, 3), (4, 4), (4, 5), (4, 6), (5, 5), (6, 6), (7, 7), 
	(7, 8), (7, 9), (8, 8), (9, 9), (10, 10), (10, 11), 
	(10, 12), (11, 11), (12, 12);

INSERT INTO rules (name, antecedent_id, consequent_id) VALUES 
	('возраст не молодой и время позднее, активность низкая', 1, 10);