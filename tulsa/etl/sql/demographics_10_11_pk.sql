--10-11 PK with Demographics
BEGIN;
DROP TABLE IF EXISTS clean_data.demographics_10_11_pk;
CREATE TABLE clean_data.demographics_10_11_pk AS
SELECT
    "Id" AS id
    , "Student Number" AS student_number
    , CAST("State Studentnumber" AS INT) AS state_student_number
    , "Last Name" AS last_name
    , CAST(NULL AS TEXT) AS middle_name
    , "First Name" AS first_name
    , "Street" AS street
    , "City" AS city
    , CAST(SPLIT_PART("Zip", '-', 1) AS INT) AS zip
    , TO_DATE("Dob", 'YYYY-MM-DD') AS dob
    , "Gender" AS gender
    , "Ethnicity" AS ethnicity
    , CASE "Tps Ell Other Lang Spoken" 
        WHEN 'v1' THEN 'no'
        WHEN 'v4' THEN 'yes, more often'
        WHEN 'v5' THEN 'yes, less often'
    END AS tps_ell_other_lang_spoken
    , "Ok Ell Language Code" AS ok_ell_language_code
    , CASE "Lunchstatus" 
        WHEN 'P' THEN 'paid'
        WHEN 'F' THEN 'free'
        WHEN 'R' THEN 'reduced'
    END AS lunch_status
    , "Ok Idea" AS ok_idea
    , CAST(NULL AS TEXT) AS ok_primary_disability_code
    , CAST(NULL AS TEXT) AS tps_service_delivery_code
    , CASE "Ok Ell"
        WHEN 'YES' THEN 'yes'
        WHEN 'NO' THEN 'no'
        ELSE NULL
    END AS ok_ell
    , CAST(NULL AS TEXT) AS ok_homeless
    , CAST(NULL AS TEXT) AS tps_demographics_lives_with
    , "Grade Level" AS grade_level
    , "Schoolid" AS school_id
    , CAST(NULL AS TEXT) AS school_name
    , CAST(NULL AS TEXT) AS school_address
    , CAST(NULL AS INT) AS school_zip
    , TO_DATE(CAST("Entrydate" AS TEXT), 'YYYY-MM-DD') AS entry_date
    , CAST("Entrycode" AS TEXT) AS entry_code
    , CAST(NULL AS TEXT) AS transfer_comment
    , TO_DATE(CAST("Exitdate" AS TEXT), 'YYYY-MM-DD') AS exit_date
    , CAST("Exitcode" AS TEXT) AS exit_code
    , CAST(NULL AS TEXT) AS exit_comment
FROM
    raw_data."demographics_10_11_10-11_pk_with_demographics";
COMMIT;
