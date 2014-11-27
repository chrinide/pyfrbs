SELECT * FROM nodes
	JOIN closures ON nodes.id = closures.descendant_id
WHERE closures.ancestor_id IN (
	SELECT antecedent_id FROM rules WHERE id = 1
) ORDER BY parent_id ASC;
SELECT * FROM nodes
	JOIN closures ON nodes.id = closures.descendant_id
WHERE closures.ancestor_id IN (
	SELECT consequent_id FROM rules WHERE id = 1
) ORDER BY parent_id ASC;
