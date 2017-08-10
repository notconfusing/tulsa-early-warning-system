--12-13 PK to 1st Demographics
BEGIN;
DROP TABLE IF EXISTS clean_data.demographics_12_13_pk_1st;
CREATE TABLE clean_data.demographics_12_13_pk_1st AS
SELECT
    id
    , student_number
    , CAST(state_studentnumber AS INT) AS state_student_number
    , last_name
    , middle_name
    , first_name
    , street
    , city
    , CASE zip 
        WHEN 'undefined' THEN NULL
        ELSE CAST(SPLIT_PART(zip, '-', 1) AS INT) 
    END AS zip
    , TO_DATE(dob, 'MM/DD/YYYY') AS dob
    , gender
    , ethnicity
    , CASE tps_ell_other_lang_spoken
        WHEN 'v1' THEN 'no'
        WHEN 'v4' THEN 'yes, more often'
        WHEN 'v5' THEN 'yes, less often'
    END AS tps_ell_other_lang_spoken
    , ok_ell_language_code
    , CASE lunchstatus
        WHEN 'P' THEN 'paid'
        WHEN 'F' THEN 'free'
        WHEN 'R' THEN 'reduced'
    END AS lunch_status
    , ok_idea
    , CASE ok_primarydisabilitycode
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
    , CASE tps_seas_service_delivery_code
        WHEN 1 THEN 'regular class full time'
        WHEN 2 THEN 'regular class full time'
        WHEN 3 THEN 'special class part time'
        WHEN 4 THEN 'special class full time'
        WHEN 5 THEN 'special class full time'
        WHEN 6 THEN 'outside of public school setting'
        WHEN 7 THEN 'preschool continuum'
        ELSE NULL
    END AS tps_service_delivery_code
    , CASE ok_ell
        WHEN 2349 THEN 'yes'
        WHEN 1633 THEN 'no'
        WHEN 1634 THEN 'took placement but did not qualify'
        WHEN 1636 THEN 'former ell but tested out'
        WHEN 9997 THEN 'pending testing - qualification unknown'
        ELSE NULL
    END AS ok_ell
    , ok_homeless
    , CASE tps_demographics_lives_with
        WHEN 1 THEN 'both parents'
        WHEN 2 THEN 'mother'
        WHEN 3 THEN 'father'
        WHEN 4 THEN 'court guardian or DHS custody'
        WHEN 5 THEN 'other'
        WHEN 6 THEN 'affidavit'
        ELSE NULL
    END AS tps_demographics_lives_with
    , grade_level
    , schoolid AS school_id
    , "39name" AS school_name
    , "39schooladdress" AS school_address
    , "39schoolzip" AS school_zip
    , CAST(NULL AS DATE) AS entry_date
    , CAST(NULL AS TEXT) AS entry_code
    , CAST(NULL AS TEXT) AS transfer_comment
    , CAST(NULL AS DATE) AS exit_date
    , CAST(NULL AS TEXT) AS exit_code
    , CAST(NULL AS TEXT) AS exit_comment
FROM
    raw_data.demographics_12_13;
COMMIT;