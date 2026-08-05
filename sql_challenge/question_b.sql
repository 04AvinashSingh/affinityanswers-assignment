
-- Question B: Which type of wheat has the longest DNA sequence?
-- (hint: use the rfamseq and the taxonomy tables)

-- Answer: Triticum durum (durum wheat) — 836,514,780 bp


SELECT t.species, MAX(rs.length) AS max_length
FROM rfamseq rs
JOIN taxonomy t ON rs.ncbi_id = t.ncbi_id
WHERE t.species LIKE '%Triticum%'
GROUP BY t.species
ORDER BY max_length DESC;
