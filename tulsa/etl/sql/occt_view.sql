BEGIN;
DROP VIEW IF EXISTS clean_data.occt;
CREATE VIEW clean_data.occt AS
SELECT
    last_name
    , first_name
    , middle_initial
    , student_id_state
    , student_id_local
    , district_name
    , school_name
    , grade
    , birth_date
    , 'Reading' AS discipline
    , reading_raw_score AS raw_score
    , reading_opi AS scale_score
    , reading_performance_level AS performance_level
    , reading_form AS form
    , 2015 AS cal_year
FROM
    clean_data.occt_2015


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , student_id_state
    , student_id_local
    , district_name
    , school_name
    , grade
    , birth_date
    , 'Math' AS discipline
    , mathematics_raw_score AS raw_score
    , mathematics_opi AS scale_score
    , mathematics_performance_level AS performance_level
    , mathematics_form AS form
    , 2015 AS cal_year
FROM
    clean_data.occt_2015


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , student_id_state
    , student_id_local
    , district_name
    , school_name
    , grade
    , birth_date
    , TRIM(TRAILING ' ' FROM discipline) AS discipline
    , raw_score
    , scale_score
    , performance_level
    , form
    , 2014 AS cal_year
FROM
    clean_data.occt_2014    
WHERE
    discipline LIKE 'Reading%'
    OR discipline LIKE 'Math%'


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , student_id_state
    , student_id_local
    , district_name
    , school_name
    , grade
    , birth_date
    , TRIM(TRAILING ' ' FROM discipline) AS discipline
    , raw_score
    , scale_score
    , performance_level
    , form
    , 2013 AS cal_year
FROM
    clean_data.occt_2013
WHERE
    discipline LIKE 'Reading%'
    OR discipline LIKE 'Math%';
COMMIT;