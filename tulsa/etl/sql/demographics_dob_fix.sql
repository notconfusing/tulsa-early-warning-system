BEGIN;

-- Remove unrealistic date entries
UPDATE clean_data.demographics_10_11_pk
  SET dob = NULL
  WHERE dob < TO_DATE('1970-01-01', 'YYYY-MM-DD');

UPDATE clean_data.demographics_11_12_pk_k
  SET dob = NULL
  WHERE dob < TO_DATE('1970-01-01', 'YYYY-MM-DD');

-- Create correct DOB temp table for later UPDATE statements
-- Starting with "majority rules"
CREATE TEMPORARY TABLE correct_dob AS 
  (WITH stu_dob AS
  (
      SELECT
          student_number,
          COUNT(DISTINCT dob) as dob_ct
      FROM
          clean_data.demographics
      GROUP BY
          student_number
      HAVING
          COUNT(DISTINCT dob) > 1
  ),
  right_dob AS (
      SELECT
          student_number,
          dob,
          COUNT(*) AS entry_ct
      FROM    
          clean_data.demographics
          INNER JOIN stu_dob 
              USING (student_number)
      GROUP BY
          student_number, dob
      HAVING COUNT(*) > 1
      ORDER BY
          student_number, dob
  ),
  wrong_dob AS
  (SELECT
      student_number,
      dob,
      COUNT(*) AS entry_ct
  FROM    
      clean_data.demographics
      INNER JOIN stu_dob 
          USING (student_number)
  GROUP BY
      student_number, dob
  HAVING COUNT(*) = 1
  ORDER BY
      student_number, dob)


  SELECT
      student_number,
      right_dob.dob as right_dob,
      measured_year
  FROM
      clean_data.demographics
      INNER JOIN wrong_dob
          USING (student_number, dob)
      LEFT JOIN right_dob 
          USING (student_number)
  WHERE
      right_dob.dob IS NOT NULL); 

-- Correcting this specific student's bad DOB entry
INSERT INTO correct_dob VALUES
(637060, NULL, '12_13');

-- UPDATE statements for underlying dem tables
-- based on correct_dob table
UPDATE clean_data.demographics_10_11_pk
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_10_11_pk.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '10_11';

UPDATE clean_data.demographics_11_12_pk_k
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_11_12_pk_k.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '11_12';

UPDATE clean_data.demographics_12_13_pk_1st
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_12_13_pk_1st.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '12_13';

UPDATE clean_data.demographics_13_14_pk_2nd
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_13_14_pk_2nd.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '13_14';

UPDATE clean_data.demographics_14_15_pk_3rd
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_14_15_pk_3rd.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '14_15';

UPDATE clean_data.demographics_15_16_pk_4th
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_15_16_pk_4th.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '15_16';

-- Truncate correct DOB temp table to make room for "most recent" strategy
TRUNCATE correct_dob;

-- Insert "most recent" DOB for all other students with conflicting DOBs
INSERT INTO correct_dob
WITH multi_dob_students AS
(
    SELECT
        student_number
    FROM
        clean_data.demographics
    GROUP BY
        student_number
    HAVING
        COUNT(DISTINCT dob) > 1
),
students AS
(
    SELECT
        student_number,
        dob,
        measured_year
    FROM
        clean_data.demographics
        INNER JOIN multi_dob_students
            USING (student_number)
),
min_year AS
(
    SELECT
        student_number,
        MIN(measured_year) AS min_year
    FROM
        students
    GROUP BY
        student_number
)

SELECT
    student_number,
    dob AS right_dob,
    min_year AS measured_year
FROM
    students
    LEFT JOIN min_year
        USING (student_number)
WHERE
    measured_year <> min_year;

-- UPDATE statements for underlying dem tables
UPDATE clean_data.demographics_10_11_pk
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_10_11_pk.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '10_11';

UPDATE clean_data.demographics_11_12_pk_k
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_11_12_pk_k.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '11_12';

UPDATE clean_data.demographics_12_13_pk_1st
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_12_13_pk_1st.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '12_13';

UPDATE clean_data.demographics_13_14_pk_2nd
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_13_14_pk_2nd.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '13_14';

UPDATE clean_data.demographics_14_15_pk_3rd
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_14_15_pk_3rd.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '14_15';

UPDATE clean_data.demographics_15_16_pk_4th
SET dob = correct_dob.right_dob
FROM correct_dob
WHERE clean_data.demographics_15_16_pk_4th.student_number = correct_dob.student_number
    AND correct_dob.measured_year = '15_16';

COMMIT;