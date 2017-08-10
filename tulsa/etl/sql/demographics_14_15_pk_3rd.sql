--14-15 PK to 3rd Demographics
BEGIN;
DROP TABLE IF EXISTS clean_data.demographics_14_15_pk_3rd;
CREATE TABLE clean_data.demographics_14_15_pk_3rd AS
SELECT
    data."ID" AS id
    , data."Student_number" AS student_number
    , CAST(data."State_StudentNumber" AS INT) AS state_student_number
    , data."Last_name" AS last_name
    , data."Middle_name" AS middle_name
    , data."First_name" AS first_name
    , data."Street" AS street
    , data."City" AS city
    , CAST(data."Zip" AS INT) AS zip
    , TO_DATE(CAST(data."DOB" AS TEXT), 'MM/DD/YYYY') AS dob
    , data."Gender" AS gender
    , data."Ethnicity" AS ethnicity
    , CASE data."TPS_ELL_Other_Lang_Spoken" 
        WHEN 'v1' THEN 'no'
        WHEN 'v4' THEN 'yes, more often'
        WHEN 'v5' THEN 'yes, less often'
    END AS tps_ell_other_lang_spoken
    , data."OK_ELL_Language_Code" AS ok_ell_language_code
    , CASE data."LunchStatus" 
        WHEN 'P' THEN 'paid'
        WHEN 'F' THEN 'free'
        WHEN 'R' THEN 'reduced'
    END AS lunch_status
    , data."OK_Idea" AS ok_idea
    , CASE data."OK_PRIMARYDISABILITYCODE"
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
    , CASE data."TPS_SEAS_SERVICE_DELIVERY_CODE"
        WHEN 1 THEN 'regular class full time'
        WHEN 2 THEN 'regular class full time'
        WHEN 3 THEN 'special class part time'
        WHEN 4 THEN 'special class full time'
        WHEN 5 THEN 'special class full time'
        WHEN 6 THEN 'outside of public school setting'
        WHEN 7 THEN 'preschool continuum'
        ELSE NULL
    END AS tps_service_delivery_code
    , CASE data."OK_ELL"
        WHEN 2349 THEN 'yes'
        WHEN 1633 THEN 'no'
        WHEN 1634 THEN 'took placement but did not qualify'
        WHEN 1636 THEN 'former ell but tested out'
        WHEN 9997 THEN 'pending testing - qualification unknown'
        ELSE NULL
    END AS ok_ell
    , data."OK_Homeless" AS ok_homeless
    , CASE data."TPS_Demographics_lives_with" 
        WHEN 1 THEN 'both parents'
        WHEN 2 THEN 'mother'
        WHEN 3 THEN 'father'
        WHEN 4 THEN 'court guardian or DHS custody'
        WHEN 5 THEN 'other'
        WHEN 6 THEN 'affidavit'
        ELSE NULL
    END AS tps_demographics_lives_with
    , data."Grade_Level" AS grade_level
    , data."Schoolid" AS school_id
    , data."[39]name" AS school_name
    , data."[39]SchoolAddress" AS school_address
    , data."[39]SchoolZip" AS school_zip
    , TO_DATE(CAST(codes."EntryDate" AS TEXT), 'YYYY-MM-DD') AS entry_date
    , CAST(codes."EntryCode" AS TEXT) AS entry_code
    , CAST(NULL AS TEXT) AS transfer_comment
    , TO_DATE(CAST(codes."ExitDate" AS TEXT), 'YYYY-MM-DD') AS exit_date
    , CAST(codes."ExitCode" AS TEXT) AS exit_code
    , CAST(NULL AS TEXT) AS exit_comment
FROM
    raw_data.demographics_14_15_pk_3rd AS data
    INNER JOIN raw_data."demographics_14_15_14-15_pk_to_3rd_demographics" AS codes
        USING ("Student_number");
COMMIT;