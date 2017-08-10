BEGIN;
DROP TABLE IF EXISTS clean_data.occt_2015;

CREATE TABLE clean_data.occt_2015 AS

SELECT
    last_name
    , first_name
    , middle_initial
    , CAST(student_id_state AS INT)
    , CASE 
        WHEN studen_id_local !~ '[a-zA-z ]'
            THEN CAST(studen_id_local AS INT)
        ELSE NULL
    END AS student_id_local
    , district_name
    , school_name
    , CASE grade
        WHEN 'Unknown Grade' THEN NULL
        ELSE CAST(REPLACE(grade, 'Grade ', '') AS INT) 
    END AS grade
    , birth_date
    , gender
    , ethnicity
    , economically_disadvantaged
    , ell
    , iep
    , "504" AS c_504
    , ell_proficient
    , fay_in_state
    , fay_in_district
    , fay_in_school
    , regular_education
    , alt_ed_academy
    , migrant
    , "title_x,_part_c" AS title_x
    , other_placement
    , CASE 
        WHEN reading_raw_score !~ '[a-zA-z ]'
            THEN CAST(reading_raw_score AS INT)
        ELSE NULL
    END AS reading_raw_score
    , CASE 
        WHEN reading_opi !~ '[a-zA-z ]'
            THEN CAST(reading_opi AS INT)
        ELSE NULL
    END AS reading_opi
    , reading_performance_level
    , re40
    , re42
    , re43
    , re50
    , reading_class_name
    , reading_form
    , reading_mode
    , reading_condition_code
    , reading_ell_accommodations
    , reading_504_accommodations
    , reading_iep_accommodations
    , reading__non_standard_read_aloud_accommodation
    , CASE 
        WHEN mathematics_raw_score !~ '[a-zA-z ]'
            THEN CAST(mathematics_raw_score AS INT)
        ELSE NULL
    END AS mathematics_raw_score
    , CASE 
        WHEN mathematics_opi !~ '[a-zA-z ]'
            THEN CAST(mathematics_opi AS INT)
        ELSE NULL
    END mathematics_opi
    , mathematics_performance_level
    , ma10
    , ma11
    , ma12
    , ma20
    , ma21
    , ma22
    , ma30
    , ma31
    , ma32
    , ma40
    , ma41
    , ma42
    , ma50
    , ma51
    , mathematics_class_name
    , mathematics_form
    , mathematics__mode
    , mathematics_condition_code
    , mathematics_ell_accommodations
    , mathematics_504_accommodations
    , mathematics_iep_accommodations
FROM
    raw_data.occt_2015_3rd_grade_3_occt


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , CAST(student_id_state AS INT)
    , CAST(student_id_local AS INT)
    , district_name
    , school_name
    , CASE grade
        WHEN 'Unknown Grade' THEN NULL
        ELSE CAST(REPLACE(grade, 'Grade ', '') AS INT) 
    END AS grade
    , birth_date
    , gender
    , ethnicity
    , economically_disadvantaged
    , ell
    , iep
    , "504" AS c_504
    , ell_proficient
    , fay_in_state
    , fay_in_district
    , fay_in_school
    , regular_education
    , alt_ed_academy
    , migrant
    , "title_x,_part_c" AS title_x
    , other_placement
    , CASE 
        WHEN reading_raw_score !~ '[a-zA-z ]'
            THEN CAST(reading_raw_score AS INT)
        ELSE NULL
    END AS reading_raw_score
    , CASE 
        WHEN reading_opi !~ '[a-zA-z ]'
            THEN CAST(reading_opi AS INT)
        ELSE NULL
    END AS reading_opi
    , reading_performance_level
    , re40
    , re42
    , re43
    , re50
    , reading_class_name
    , reading_form
    , reading_mode
    , reading_condition_code
    , reading_ell_accommodations
    , reading_504_accommodations
    , reading_iep_accommodations
    , reading__non_standard_read_aloud_accommodation
    , CASE 
        WHEN mathematics_raw_score !~ '[a-zA-z ]'
            THEN CAST(mathematics_raw_score AS INT)
        ELSE NULL
    END AS mathematics_raw_score
    , CASE 
        WHEN mathematics_opi !~ '[a-zA-z ]'
            THEN CAST(mathematics_opi AS INT)
        ELSE NULL
    END mathematics_opi
    , mathematics_performance_level
    , ma10
    , ma11
    , ma12
    , ma20
    , ma21
    , ma22
    , ma30
    , ma31
    , ma32
    , ma40
    , ma41
    , ma42
    , ma50
    , ma51
    , mathematics_class_name
    , mathematics_form
    , mathematics__mode
    , mathematics_condition_code
    , mathematics_ell_accommodations
    , mathematics_504_accommodations
    , mathematics_iep_accommodations
FROM
    raw_data.occt_2015_4th_grade_4_occt


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , CAST(student_id_state AS INT)
    , CASE 
        WHEN studen_id_local !~ '[a-zA-z ]'
            THEN CAST(studen_id_local AS INT)
        ELSE NULL
    END AS student_id_local
    , district_name
    , school_name
    , CASE grade
        WHEN 'Unknown Grade' THEN NULL
        ELSE CAST(REPLACE(grade, 'Grade ', '') AS INT) 
    END AS grade
    , birth_date
    , gender
    , ethnicity
    , economically_disadvantaged
    , ell
    , iep
    , "504" AS c_504
    , ell_proficient
    , fay_in_state
    , fay_in_district
    , fay_in_school
    , regular_education
    , alt_ed_academy
    , migrant
    , "title_x,_part_c" AS title_x
    , other_placement
    , CASE 
        WHEN reading_raw_score !~ '[a-zA-z ]'
            THEN CAST(reading_raw_score AS INT)
        ELSE NULL
    END AS reading_raw_score
    , CASE 
        WHEN reading_opi !~ '[a-zA-z ]'
            THEN CAST(reading_opi AS INT)
        ELSE NULL
    END AS reading_opi
    , reading_performance_level
    , re40
    , re42
    , re43
    , re50
    , reading_class_name
    , reading_form
    , reading_mode
    , reading_condition_code
    , reading_ell_accommodations
    , reading_504_accommodations
    , reading_iep_accommodations
    , reading__non_standard_read_aloud_accommodation
    , CASE 
        WHEN mathematics_raw_score !~ '[a-zA-z ]'
            THEN CAST(mathematics_raw_score AS INT)
        ELSE NULL
    END AS mathematics_raw_score
    , CASE 
        WHEN mathematics_opi !~ '[a-zA-z ]'
            THEN CAST(mathematics_opi AS INT)
        ELSE NULL
    END mathematics_opi
    , mathematics_performance_level
    , ma10
    , ma11
    , ma12
    , ma20
    , ma21
    , ma22
    , ma30
    , ma31
    , ma32
    , ma40
    , ma41
    , ma42
    , ma50
    , ma51
    , mathematics_class_name
    , mathematics_form
    , mathematics__mode
    , mathematics_condition_code
    , mathematics_ell_accommodations
    , mathematics_504_accommodations
    , mathematics_iep_accommodations
FROM
    raw_data.occt_2015_5th_grade_5_occt


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , CAST(student_id_state AS INT)
    , CAST(studen_id_local AS INT) AS student_id_local
    , district_name
    , school_name
    , CASE grade
        WHEN 'Unknown Grade' THEN NULL
        ELSE CAST(REPLACE(grade, 'Grade ', '') AS INT) 
    END AS grade
    , birth_date
    , gender
    , ethnicity
    , economically_disadvantaged
    , ell
    , iep
    , "504" AS c_504
    , ell_proficient
    , fay_in_state
    , fay_in_district
    , fay_in_school
    , regular_education
    , alt_ed_academy
    , migrant
    , "title_x,_part_c" AS title_x
    , other_placement
    , CASE 
        WHEN reading_raw_score !~ '[a-zA-z ]'
            THEN CAST(reading_raw_score AS INT)
        ELSE NULL
    END AS reading_raw_score
    , CASE 
        WHEN reading_opi !~ '[a-zA-z ]'
            THEN CAST(reading_opi AS INT)
        ELSE NULL
    END AS reading_opi
    , reading_performance_level
    , re40
    , re42
    , re43
    , re50
    , reading_class_name
    , reading_form
    , reading_mode
    , reading_condition_code
    , reading_ell_accommodations
    , reading_504_accommodations
    , reading_iep_accommodations
    , reading__non_standard_read_aloud_accommodation
    , CASE 
        WHEN mathematics_raw_score !~ '[a-zA-z ]'
            THEN CAST(mathematics_raw_score AS INT)
        ELSE NULL
    END AS mathematics_raw_score
    , CASE 
        WHEN mathematics_opi !~ '[a-zA-z ]'
            THEN CAST(mathematics_opi AS INT)
        ELSE NULL
    END mathematics_opi
    , mathematics_performance_level
    , ma10
    , ma11
    , ma12
    , ma20
    , ma21
    , ma22
    , ma30
    , ma31
    , ma32
    , ma40
    , ma41
    , ma42
    , ma50
    , ma51
    , mathematics_class_name
    , mathematics_form
    , mathematics__mode
    , mathematics_condition_code
    , mathematics_ell_accommodations
    , mathematics_504_accommodations
    , mathematics_iep_accommodations
FROM
    raw_data.occt_2015_6th_grade_6_occt


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , CAST(student_id_state AS INT)
    , CASE 
        WHEN studen_id_local !~ '[a-zA-z ]'
            THEN CAST(studen_id_local AS INT)
        ELSE NULL
    END AS student_id_local
    , district_name
    , school_name
    , CASE grade
        WHEN 'Unknown Grade' THEN NULL
        ELSE CAST(REPLACE(grade, 'Grade ', '') AS INT) 
    END AS grade
    , birth_date
    , gender
    , ethnicity
    , economically_disadvantaged
    , ell
    , iep
    , "504" AS c_504
    , ell_proficient
    , fay_in_state
    , fay_in_district
    , fay_in_school
    , regular_education
    , alt_ed_academy
    , migrant
    , "title_x,_part_c" AS title_x
    , other_placement
    , CASE 
        WHEN reading_raw_score !~ '[a-zA-z ]'
            THEN CAST(reading_raw_score AS INT)
        ELSE NULL
    END AS reading_raw_score
    , CASE 
        WHEN reading_opi !~ '[a-zA-z ]'
            THEN CAST(reading_opi AS INT)
        ELSE NULL
    END AS reading_opi
    , reading_performance_level
    , re40
    , re42
    , re43
    , re50
    , reading_class_name
    , reading_form
    , reading_mode
    , reading_condition_code
    , reading_ell_accommodations
    , reading_504_accommodations
    , reading_iep_accommodations
    , reading__non_standard_read_aloud_accommodation
    , CASE 
        WHEN mathematics_raw_score !~ '[a-zA-z ]'
            THEN CAST(mathematics_raw_score AS INT)
        ELSE NULL
    END AS mathematics_raw_score
    , CASE 
        WHEN mathematics_opi !~ '[a-zA-z ]'
            THEN CAST(mathematics_opi AS INT)
        ELSE NULL
    END mathematics_opi
    , mathematics_performance_level
    , ma10
    , ma11
    , ma12
    , ma20
    , ma21
    , ma22
    , ma30
    , ma31
    , ma32
    , ma40
    , ma41
    , ma42
    , ma50
    , ma51
    , mathematics_class_name
    , mathematics_form
    , mathematics__mode
    , mathematics_condition_code
    , mathematics_ell_accommodations
    , mathematics_504_accommodations
    , mathematics_iep_accommodations
FROM
    raw_data.occt_2015_7th_grade_7_occt


UNION


SELECT
    last_name
    , first_name
    , middle_initial
    , CAST(student_id_state AS INT)
    , CASE 
        WHEN studen_id_local !~ '[a-zA-z ]'
            THEN CAST(studen_id_local AS INT)
        ELSE NULL
    END AS student_id_local
    , district_name
    , school_name
    , CASE grade
        WHEN 'Unknown Grade' THEN NULL
        ELSE CAST(REPLACE(grade, 'Grade ', '') AS INT) 
    END AS grade
    , birth_date
    , gender
    , ethnicity
    , economically_disadvantaged
    , ell
    , iep
    , "504" AS c_504
    , ell_proficient
    , fay_in_state
    , fay_in_district
    , fay_in_school
    , regular_education
    , alt_ed_academy
    , migrant
    , "title_x,_part_c" AS title_x
    , other_placement
    , CASE 
        WHEN reading_raw_score !~ '[a-zA-z ]'
            THEN CAST(reading_raw_score AS INT)
        ELSE NULL
    END AS reading_raw_score
    , CASE 
        WHEN reading_opi !~ '[a-zA-z ]'
            THEN CAST(reading_opi AS INT)
        ELSE NULL
    END AS reading_opi
    , reading_performance_level
    , re40
    , re42
    , re43
    , re50
    , reading_class_name
    , reading_form
    , reading_mode
    , reading_condition_code
    , reading_ell_accommodations
    , reading_504_accommodations
    , reading_iep_accommodations
    , reading__non_standard_read_aloud_accommodation
    , CASE 
        WHEN mathematics_raw_score !~ '[a-zA-z ]'
            THEN CAST(mathematics_raw_score AS INT)
        ELSE NULL
    END AS mathematics_raw_score
    , CASE 
        WHEN mathematics_opi !~ '[a-zA-z ]'
            THEN CAST(mathematics_opi AS INT)
        ELSE NULL
    END mathematics_opi
    , mathematics_performance_level
    , ma10
    , ma11
    , ma12
    , ma20
    , ma21
    , ma22
    , ma30
    , ma31
    , ma32
    , ma40
    , ma41
    , ma42
    , ma50
    , ma51
    , mathematics_class_name
    , mathematics_form
    , mathematics__mode
    , mathematics_condition_code
    , mathematics_ell_accommodations
    , mathematics_504_accommodations
    , mathematics_iep_accommodations
FROM
    raw_data.occt_2015_8th_grade_8_occt;
COMMIT;