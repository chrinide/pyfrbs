INSERT INTO groups (is_variable, is_term, is_hedge) VALUES
	(true, false, false),
	(true, false, false),
	(true, false, false),
	(false, true, false),
	(false, true, false),
	(false, true, false),
	(false, false, true);

INSERT INTO synonims (group_id, lemma, grammemes, hits) VALUES
	(1, 'возраст', 'сущ еч', 1),
	(1, 'годы', 'сущ мч', 1),
	(2, 'время', 'сущ еч', 1),
	(2, 'часы', 'сущ мч', 1),
	(3, 'активность', 'сущ еч', 1),
	(4, 'молодой', 'прил', 1),
	(4, 'юный', 'прил', 1),
	(5, 'поздний', 'прил', 1),
	(6, 'низкий', 'прил', 1),
	(7, 'не', 'част', 1);

INSERT INTO variables (name_id, name, validated, min, max) VALUES 
	(1, 'возраст, годы', false, 0, 100),
	(2, 'время, часы', false, 0, 24),
	(3, 'активность', false, 0, 10);

INSERT INTO terms (name_id, name, validated, function_id, points) VALUES 
	(4, 'молодой, юный', false, 4, '15;20;25;30'),
	(5, 'поздний', false, 4, '0;1;3;4'),
	(6, 'низкий', false, 4, '0;1;2;3');

INSERT INTO variables_terms (variable_id, term_id) VALUES
	(1, 1),
	(2, 2),
	(3, 3);

INSERT INTO hedges (name_id, name, validated, result) VALUES 
	(7, 'не', false, '1 - x');

INSERT INTO variables_hedges (variable_id, hedge_id) VALUES 
	(1, 1);

INSERT INTO nodes (parent_id, type_id, variable_id, term_id, hedge_id) VALUES
	(null, 8, null, null, null), (1, 5, null, null, null), 
	(2, 1, 1, null, null), (2, 4, null, null, null), 
	(4, 2, null, null, 1), (4, 3, null, 1, null), 
	(1, 5, null, null, null), (7, 1, 2, null, null), 
	(7, 3, null, 2, null), (null, 5, null, null, null), 
	(10, 1, 3, null, null), (10, 3, null, 3, null);

INSERT INTO closures (ancestor_id, descendant_id) VALUES
	(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
	(1, 8), (1, 9), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
	(3, 3), (4, 4), (4, 5), (4, 6), (5, 5), (6, 6), (7, 7), 
	(7, 8), (7, 9), (8, 8), (9, 9), (10, 10), (10, 11), 
	(10, 12), (11, 11), (12, 12);

INSERT INTO rules (name, validated, antecedent_id, consequent_id) VALUES 
	('ЕСЛИ возраст не молодой и время позднее, TO активность низкая', false, 1, 10);
