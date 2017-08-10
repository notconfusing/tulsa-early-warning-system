BEGIN;
DROP TABLE IF EXISTS clean_data.occt_2014;
CREATE TABLE clean_data.occt_2014 AS
SELECT
    lastname____________ AS last_name
    , firstname AS first_name
    , middleinitial AS middle_initial
    , statestudentid AS student_id_state
    , CASE 
        WHEN localstudentid = CAST(REPLACE(localstudentid, ' ', '') AS TEXT)
            THEN NULL
        WHEN localstudentid ~ '[-]'
            THEN NULL
        WHEN REPLACE(localstudentid, ' ', '') = ''
            THEN NULL
        WHEN REPLACE(localstudentid, ' ', '') = ''
            THEN NULL
        ELSE CAST(REPLACE(localstudentid, ' ', '') AS BIGINT)
    END AS student_id_local
    , districtname_______________________ AS district_name
    , schoolname_________________________ AS school_name
    , grade
    , TO_DATE(dateofbirth,'MM/DD/YYYY') AS birth_date 
    , ell
    , iep 
    , "504" AS c_504
    , ellproficient AS ell_proficient
    , altedacademy AS alt_ed_academy
    , migrant
    , titlex
    , otherplacement AS other_placement
    , REPLACE(subject____________, 'OCCT ', '') AS discipline
    , CASE
        WHEN REPLACE(rawscore, ' ', '') = ''
            THEN NULL
        WHEN rawscore ~ '[-]'
            THEN NULL
        ELSE CAST(rawscore AS INT)
    END AS raw_score
    , CASE
        WHEN REPLACE(scalescore, ' ', '') = ''
            THEN NULL
        WHEN scalescore ~ '[-]'
            THEN NULL
        ELSE CAST(scalescore AS INT)
    END AS scale_score
    , CASE performancelevel 
        WHEN 1 THEN 'Unsatisfactory'
        WHEN 2 THEN 'Limited Knowledge'
        WHEN 3 THEN 'Proficient'
        WHEN 4 THEN 'Advanced'
        ELSE NULL
    END AS performance_level
    , CASE form
        WHEN 'B' THEN 'Braille'
        WHEN 'A' THEN 'Equivalent'
        WHEN 'Z' THEN 'Operational'
        ELSE NULL
    END AS form
FROM
    raw_data.occt_2014_3rd_8th;
UPDATE clean_data.occt_2014
SET student_id_local = CAST(REPLACE(CAST(student_id_local AS TEXT), '0000', '') AS INT)
WHERE LENGTH(CAST(student_id_local AS TEXT)) > 6;
COMMIT;