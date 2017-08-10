BEGIN;
DROP TABLE IF EXISTS clean_data.occt_2013;
CREATE TABLE clean_data.occt_2013 AS
SELECT
    lastname____________ AS last_name
    , firstname AS first_name
    , middleinitial AS middle_initial
    , CASE 
        WHEN statestudentid !~ '[a-zA-z ]'
            THEN CAST(statestudentid AS INT)
        ELSE NULL
    END AS student_id_state
    , CASE 
        WHEN localstudentid !~ '[a-zA-z ]'
            THEN CAST(localstudentid AS BIGINT)
        ELSE NULL
    END AS student_id_local
    , districtname_______________________ AS district_name
    , schoolname_________________________ AS school_name
    , grade
    , CASE 
        WHEN dateofbirth ILIKE '%/  /%' THEN NULL 
        ELSE TO_DATE(dateofbirth, 'YYYY-MM-DD') 
    END AS birth_date 
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
        WHEN rawscore !~ '[a-zA-z ]'
            THEN CAST(rawscore AS INT)
        ELSE NULL
    END AS raw_score
    , CASE
        WHEN scalescore !~ '[a-zA-z ]'
            THEN CAST(scalescore AS INT) 
        ELSE NULL
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
    raw_data.occt_2013_3rd_8th_ok_3_8_spring_2013_dist_72i001_;
COMMIT;