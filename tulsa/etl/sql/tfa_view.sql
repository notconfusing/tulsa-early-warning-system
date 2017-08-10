DROP VIEW IF EXISTS clean_data.tfa;

CREATE VIEW clean_data.tfa AS

    SELECT
        last_first,
        school_id,
        student_number,
        grade_level,
        school_zone,
        teacher_name,
        per_att AS absent,
        per_att1 AS tardy,
        entry_date,
        exit_date,
        '14_15' AS measured_year
    FROM
        clean_data.tfa_13_14

    UNION ALL

    SELECT
        last_first,
        school_id,
        student_number,
        grade_level,
        school_zone,
        teacher_name,
        absent,
        tardy,
        entry_date,
        exit_date,
        '15_16' AS measured_year
    FROM
        clean_data.tfa_14_15;