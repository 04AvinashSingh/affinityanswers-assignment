
-- Question A: How many types of Acacia plants can be found
--            in the taxonomy table of the dataset?

-- Answer: 326


SELECT COUNT(*) AS acacia_count
FROM taxonomy
WHERE species LIKE 'Acacia %';

-- To list all Acacia species:
SELECT species
FROM taxonomy
WHERE species LIKE 'Acacia %'
ORDER BY species;
