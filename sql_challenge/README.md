# Rfam Database — SQL Challenge

SQL queries against the [Rfam public MySQL database](https://docs.rfam.org/en/latest/database.html).

## Database Connection Details

| Parameter | Value                               |
|-----------|-------------------------------------|
| Host      | `mysql-rfam-public.ebi.ac.uk`       |
| User      | `rfamro`                            |
| Password  | (none)                              |
| Port      | `4497`                              |
| Database  | `Rfam`                              |

```bash
mysql --user rfamro --host mysql-rfam-public.ebi.ac.uk --port 4497 --database Rfam
```

---

## Question A

**How many types of Acacia plants can be found in the taxonomy table of the dataset?**

### Query

```sql
SELECT COUNT(*) AS acacia_count
FROM taxonomy
WHERE species LIKE 'Acacia %';
```

### Answer

**326** types of Acacia are present in the taxonomy table.

The `taxonomy.species` column stores the binomial species name. Filtering for rows whose `species` starts with `"Acacia "` restricts results to organisms of the genus *Acacia* (Family Fabaceae).

> **See:** [`question_a.sql`](question_a.sql)

---

## Question B

**Which type of wheat has the longest DNA sequence?** *(hint: use the rfamseq and taxonomy tables)*

### Query

```sql
SELECT t.species, MAX(rs.length) AS max_length
FROM rfamseq rs
JOIN taxonomy t ON rs.ncbi_id = t.ncbi_id
WHERE t.species LIKE '%Triticum%'
GROUP BY t.species
ORDER BY max_length DESC;
```

### Answer

**Triticum durum (durum wheat)** has the longest DNA sequence at **836,514,780** base pairs.

The `rfamseq` table stores sequences and their lengths; the `taxonomy` table provides species names. They are joined on `ncbi_id`. Wheat species are members of the genus *Triticum*.

| Species | Max Length |
|---|---|
| Triticum durum (durum wheat) | 836,514,780 |
| Triticum aestivum (bread wheat) | 830,829,764 |
| Triticum urartu | 753,719,114 |
| Triticum dicoccoides | 245,486 |
| Triticum turgidum | 229,209 |

> **See:** [`question_b.sql`](question_b.sql)

---

## Question C

**Paginate a list of the family names and their longest DNA sequence lengths (descending order of length) where only families that have DNA sequence lengths greater than 1,000,000 are included. Return the 9th page with 15 results per page.** *(hint: we need the family accession ID, family name, and the maximum length in the results)*

### Query

```sql
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
```

### Explanation

- **Tables used:** `family` (accession ID & name), `rfamseq` (DNA sequence length), `full_region` (links families to sequences).
- **`GROUP BY`** aggregates by family so we can compute `MAX(rs.length)`.
- **`HAVING MAX(rs.length) > 1000000`** filters out families whose longest sequence is ≤ 1 million bp.
- **`ORDER BY max_length DESC`** sorts from longest to shortest.
- **`LIMIT 15 OFFSET 120`** returns page 9 (offset = (9 − 1) × 15 = 120).

### Sample Output (Page 9)

| rfam_acc | rfam_id | max_length |
|---|---|---|
| RF01219 | snoR100 | 836,514,780 |
| RF01220 | snoR104 | 836,514,780 |
| RF01224 | snoR80 | 836,514,780 |
| RF01227 | snoR83 | 836,514,780 |
| RF01284 | snoR8a | 836,514,780 |
| RF01286 | snoR26 | 836,514,780 |
| RF01292 | snoR2 | 836,514,780 |
| RF01300 | snoU49 | 836,514,780 |
| RF01847 | Plant_U3 | 836,514,780 |
| RF01848 | ACEA_U3 | 836,514,780 |
| RF01856 | Protozoa_SRP | 836,514,780 |
| RF01911 | MIR2118 | 836,514,780 |
| RF03160 | twister-P1 | 836,514,780 |
| RF03209 | MIR9657 | 836,514,780 |
| RF03674 | MIR5387 | 836,514,780 |

> **See:** [`question_c.sql`](question_c.sql)

---

## How to Run

1. Connect to the Rfam public database using the credentials above.
2. Execute any `.sql` file directly:

```bash
mysql --user rfamro --host mysql-rfam-public.ebi.ac.uk --port 4497 --database Rfam < question_a.sql
```

Or paste the queries into any MySQL-compatible client.
