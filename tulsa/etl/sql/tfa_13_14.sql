DELETE FROM raw_data.tfa_13_14_remington 
    WHERE "Lastfirst" = 'Lastfirst';

DROP TABLE IF EXISTS clean_data.tfa_13_14;

CREATE TABLE clean_data.tfa_13_14 AS
    
    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'academy_central' AS school_name
    FROM
        raw_data.tfa_13_14_academy_central

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'anderson' AS school_name
    FROM
        raw_data.tfa_13_14_anderson

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'bell' AS school_name
    FROM
        raw_data.tfa_13_14_bell

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'burroughs' AS school_name
    FROM
        raw_data.tfa_13_14_burroughs

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'carnegie' AS school_name
    FROM
        raw_data.tfa_13_14_carnegie

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'celia_clinton' AS school_name
    FROM
        raw_data.tfa_13_14_celia_clinton

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'gilcrease' AS school_name
    FROM
        raw_data."tfa_13_14_clc--_gilcrease"

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'kw' AS school_name
    FROM
        raw_data."tfa_13_14_clc--_kw"

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'mark_twain' AS school_name
    FROM
        raw_data."tfa_13_14_clc--_mark_twain"

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'marshall' AS school_name
    FROM
        raw_data."tfa_13_14_clc--_marshall"

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'chouteau' AS school_name
    FROM
        raw_data."tfa_13_14_clc--chouteau"

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'e_field' AS school_name
    FROM
        raw_data."tfa_13_14_clc--e_field"

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'columbus' AS school_name
    FROM
        raw_data.tfa_13_14_columbus

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'cooper' AS school_name
    FROM
        raw_data.tfa_13_14_cooper

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'disney' AS school_name
    FROM
        raw_data.tfa_13_14_disney

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'dli' AS school_name
    FROM
        raw_data.tfa_13_14_dli

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'ecdc_bunche' AS school_name
    FROM
        raw_data.tfa_13_14_ecdc_bunche

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'ecdc_porter' AS school_name
    FROM
        raw_data.tfa_13_14_ecdc_porter
        UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'eisenhower' AS school_name
    FROM
        raw_data.tfa_13_14_eisenhower

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'eliot' AS school_name
    FROM
        raw_data.tfa_13_14_eliot

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'emerson' AS school_name
    FROM
        raw_data.tfa_13_14_emerson

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'grimes' AS school_name
    FROM
        raw_data.tfa_13_14_grimes

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'grissom' AS school_name
    FROM
        raw_data.tfa_13_14_grissom

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'hamilton' AS school_name
    FROM
        raw_data.tfa_13_14_hamilton
    
    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'hawthorne' AS school_name
    FROM
        raw_data.tfa_13_14_hawthorne

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'hoover' AS school_name
    FROM
        raw_data.tfa_13_14_hoover

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'jackson' AS school_name
    FROM
        raw_data.tfa_13_14_jackson

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'jones' AS school_name
    FROM
        raw_data.tfa_13_14_jones

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'kerr' AS school_name
    FROM
        raw_data.tfa_13_14_kerr

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'key' AS school_name
    FROM
        raw_data.tfa_13_14_key
    
    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'lanier' AS school_name
    FROM
        raw_data.tfa_13_14_lanier

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'lee' AS school_name
    FROM
        raw_data.tfa_13_14_lee

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'lewis_and_clark' AS school_name
    FROM
        raw_data.tfa_13_14_lewis_and_clark

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'lindbergh' AS school_name
    FROM
        raw_data.tfa_13_14_lindbergh

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'macarthur' AS school_name
    FROM
        raw_data.tfa_13_14_macarthur

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'mayo' AS school_name
    FROM
        raw_data.tfa_13_14_mayo
    
    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'mcclure' AS school_name
    FROM
        raw_data.tfa_13_14_mcclure

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        CASE WHEN "Entrydate" ~ '^(0|[1-9][0-9]*)$'
            THEN date '1900-01-01' + CAST("Entrydate"||' DAYS' AS INTERVAL)
            ELSE TO_DATE("Entrydate", 'YYYY-MM-DD')
        END AS entry_date,
        CASE WHEN "Exitdate" ~ '^(0|[1-9][0-9]*)$'
            THEN date '1900-01-01' + CAST("Exitdate"||' DAYS' AS INTERVAL)
            ELSE TO_DATE("Exitdate", 'YYYY-MM-DD')
        END AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'mckinley' AS school_name
    FROM
        raw_data.tfa_13_14_mckinley

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'mitchell' AS school_name
    FROM
        raw_data.tfa_13_14_mitchell

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'owen' AS school_name
    FROM
        raw_data.tfa_13_14_owen

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'park' AS school_name
    FROM
        raw_data.tfa_13_14_park

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        CASE WHEN "Entrydate" ~ '^(0|[1-9][0-9]*)$'
            THEN date '1900-01-01' + CAST("Entrydate"||' DAYS' AS INTERVAL)
            ELSE TO_DATE("Entrydate", 'YYYY-MM-DD')
        END AS entry_date,
        CASE WHEN "Exitdate" ~ '^(0|[1-9][0-9]*)$'
            THEN date '1900-01-01' + CAST("Exitdate"||' DAYS' AS INTERVAL)
            ELSE TO_DATE("Exitdate", 'YYYY-MM-DD')
        END AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'patrick_henry' AS school_name
    FROM
        raw_data.tfa_13_14_patrick_henry
    
    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'peary' AS school_name
    FROM
        raw_data.tfa_13_14_peary

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'penn' AS school_name
    FROM
        raw_data.tfa_13_14_penn

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'project_accept' AS school_name
    FROM
        raw_data.tfa_13_14_project_accept

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        CAST("Ok Accreditedschool" AS INT) AS school_id,
        CAST("Student Number" AS INT) AS student_number,
        CAST("Id" AS INT) AS id,
        CAST("Grade Level" AS INT) AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        CAST("Per.att" AS INT) AS per_att,
        CAST("Per.att.1" AS INT) AS per_att1,
        TO_DATE(CAST("Entrydate" AS TEXT), 'YYYY-MM-DD') AS entry_date,
        TO_DATE(CAST("Exitdate" AS TEXT), 'YYYY-MM-DD') AS exit_date,
        "*period Info.1" AS period_info1,
        CAST("*period Info.2" AS NUMERIC) AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'remington' AS school_name
    FROM
        raw_data.tfa_13_14_remington

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'robertson' AS school_name
    FROM
        raw_data.tfa_13_14_robertson

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'salk' AS school_name
    FROM
        raw_data.tfa_13_14_salk
    
    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'sequoyah' AS school_name
    FROM
        raw_data.tfa_13_14_sequoyah

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'skelly' AS school_name
    FROM
        raw_data.tfa_13_14_skelly

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'springdale' AS school_name
    FROM
        raw_data.tfa_13_14_springdale

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'whitman' AS school_name
    FROM
        raw_data.tfa_13_14_whitman

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        CASE WHEN "Entrydate" ~ '^(0|[1-9][0-9]*)$'
            THEN date '1900-01-01' + CAST("Entrydate"||' DAYS' AS INTERVAL)
            ELSE TO_DATE("Entrydate", 'YYYY-MM-DD')
        END AS entry_date,
        CASE WHEN "Exitdate" ~ '^(0|[1-9][0-9]*)$'
            THEN date '1900-01-01' + CAST("Exitdate"||' DAYS' AS INTERVAL)
            ELSE TO_DATE("Exitdate", 'YYYY-MM-DD')
        END AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'wright' AS school_name
    FROM
        raw_data.tfa_13_14_wright

    UNION ALL

    SELECT
        "Lastfirst" AS last_first,
        "Ok Accreditedschool" AS school_id,
        "Student Number" AS student_number,
        "Id" AS id,
        "Grade Level" AS grade_level,
        "[39]name" AS school_zone,
        "*period Info" AS teacher_name,
        "Per.att" AS per_att,
        "Per.att.1" AS per_att1,
        "Entrydate" AS entry_date,
        "Exitdate" AS exit_date,
        "*period Info.1" AS period_info1,
        "*period Info.2" AS period_info2,
        "*period Info.3" AS period_info3,
        "*period Info.4" AS period_info4,
        'zarrow' AS school_name
    FROM
        raw_data.tfa_13_14_zarrow;
    