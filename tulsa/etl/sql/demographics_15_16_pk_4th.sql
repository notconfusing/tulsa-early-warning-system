-- 15-16 PK to 4th Demographics
BEGIN;
DROP TABLE IF EXISTS clean_data.demographics_15_16_pk_4th;
CREATE TABLE clean_data.demographics_15_16_pk_4th AS
SELECT
    "ID" AS id
    , "Student_number" AS student_number
    , CAST("State_StudentNumber" AS INT) AS state_student_number
    , "Last_name" AS last_name
    , "Middle_name" AS middle_name
    , "First_name" AS first_name
    , "Street" AS street
    , "City" AS city
    , CAST("Zip" AS INT) AS zip
    , TO_DATE(CAST("DOB" AS TEXT), 'YYYY-MM-DD') AS dob
    , "Gender" AS gender
    , "Ethnicity" AS ethnicity
    , CASE "TPS_ELL_Other_Lang_Spoken" 
        WHEN 'v1' THEN 'no'
        WHEN 'v4' THEN 'yes, more often'
        WHEN 'v5' THEN 'yes, less often'
    END AS tps_ell_other_lang_spoken
    , "OK_ELL_Language_Code" AS ok_ell_language_code
    , CASE "LunchStatus" 
        WHEN 'P' THEN 'paid'
        WHEN 'F' THEN 'free'
        WHEN 'R' THEN 'reduced'
    END AS lunch_status
    , "OK_Idea" AS ok_idea
    , CASE "OK_ELL"
        WHEN 2349 THEN 'yes'
        WHEN 1633 THEN 'no'
        WHEN 1634 THEN 'took placement but did not qualify'
        WHEN 1636 THEN 'former ell but tested out'
        WHEN 9997 THEN 'pending testing - qualification unknown'
        ELSE NULL
    END AS ok_ell
    , CASE "OK_PRIMARYDISABILITYCODE"
        WHEN 'PD00' THEN 'none'
        WHEN 'PD03' THEN 'hearing impairment (not including deafness)'
        WHEN 'PD04' THEN 'deafness'
        WHEN 'PD05' THEN 'speech or language impairment'
        WHEN 'PD06' THEN 'visual impairment (including blindness)'
        WHEN 'PD07' THEN 'emotional disturbance'
        WHEN 'PD08' THEN 'orthopedic impairment'
        WHEN 'PD09' THEN 'other health impairment'
        WHEN 'PD10' THEN 'specific learning disability'
        WHEN 'PD11' THEN 'deaf-blindness (both must exist)'
        WHEN 'PD12' THEN 'multiple disabilities'
        WHEN 'PD13' THEN 'autism'
        WHEN 'PD14' THEN 'traumatic brain injury'
        WHEN 'PD15' THEN 'developmental delay'
        WHEN 'PD16' THEN 'intellectually disabled'
        ELSE NULL
    END AS ok_primary_disability_code
    , CASE "TPS_SEAS_SERVICE_DELIVERY_CODE"
        WHEN 1 THEN 'regular class full time'
        WHEN 2 THEN 'regular class full time'
        WHEN 3 THEN 'special class part time'
        WHEN 4 THEN 'special class full time'
        WHEN 5 THEN 'special class full time'
        WHEN 6 THEN 'outside of public school setting'
        WHEN 7 THEN 'preschool continuum'
        ELSE NULL
    END AS tps_service_delivery_code
    , "OK_Homeless" AS ok_homeless
    , CASE "TPS_Demographics_lives_with" 
        WHEN 1 THEN 'both parents'
        WHEN 2 THEN 'mother'
        WHEN 3 THEN 'father'
        WHEN 4 THEN 'court guardian or DHS custody'
        WHEN 5 THEN 'other'
        WHEN 6 THEN 'affidavit'
        ELSE NULL
    END AS tps_demographics_lives_with
    , "Grade_Level" AS grade_level
    , "Schoolid" AS school_id
    , "[39]name" AS school_name
    , "[39]SchoolAddress" AS school_address
    , "[39]SchoolZip" AS school_zip
    , TO_DATE("entrydate", 'MM/DD/YYYY') AS entry_date
    , CAST("entrycode" AS TEXT) AS entry_code
    , "transfercomment" AS transfer_comment
    , TO_DATE("ExitDate", 'MM/DD/YYYY') AS exit_date
    , CAST("ExitCode" AS TEXT) AS exit_code
    , "ExitComment" AS exit_comment
FROM
    raw_data.demographics_15_16_pk_3rd_with_entry_exit;
COMMIT;