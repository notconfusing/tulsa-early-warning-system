DROP TABLE IF EXISTS clean_data.tfa_14_15;

CREATE TABLE clean_data.tfa_14_15 AS

    SELECT
        lastfirst AS last_first,
        ok_accreditedschool AS school_id,
        student_number,
        grade_level,
        "39name" AS school_zone,
        teacher_name,
        absent,
        tardy,
        entrydate AS entry_date,
        exitdate AS exit_date
    FROM
        raw_data.tfa_14_15_studentattendance_2;