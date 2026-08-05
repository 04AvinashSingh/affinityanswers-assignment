
-- Question C: Paginate a list of family names and their longest
--             DNA sequence lengths (descending order of length),
--             where only families with DNA sequence lengths
--             greater than 1,000,000 are included.
--
--             Return the 9th page with 15 results per page.
--             (hint: we need the family accession ID, family
--              name, and the maximum length in the results)

-- Page calculation: OFFSET = (page - 1) * page_size
--                          = (9 - 1) * 15
--                          = 120


SELECT
    f.rfam_acc,
    f.rfam_id,
    MAX(rs.length) AS max_length
FROM
    full_region fr
    JOIN rfamseq rs ON fr.rfamseq_acc = rs.rfamseq_acc
    JOIN family f   ON fr.rfam_acc    = f.rfam_acc
GROUP BY
    f.rfam_acc,
    f.rfam_id
HAVING
    MAX(rs.length) > 1000000
ORDER BY
    max_length DESC
LIMIT 15 OFFSET 120;
