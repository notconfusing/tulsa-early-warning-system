CREATE VIEW clean_data.demographics AS

    SELECT 
        city,
        dob,
        entry_code,
        entry_date,
        ethnicity,
        exit_code,
        exit_comment,
        exit_date,
        first_name,
        gender,
        grade_level,
        id,
        last_name,
        lunch_status,
        middle_name,
        school_name,
        ok_ell,
        ok_ell_language_code,
        ok_homeless,
        ok_idea,
        ok_primary_disability_code,
        school_address,
        school_id,
        school_zip,
        state_student_number,
        street,
        student_number,
        transfer_comment,
        tps_demographics_lives_with,
        tps_ell_other_lang_spoken,
        tps_service_delivery_code,
        zip,
        '10_11' AS measured_year,
        2010 AS start_year
    FROM
        clean_data.demographics_10_11_pk

    UNION ALL

    SELECT 
        city,
        dob,
        entry_code,
        entry_date,
        ethnicity,
        exit_code,
        exit_comment,
        exit_date,
        first_name,
        gender,
        grade_level,
        id,
        last_name,
        lunch_status,
        middle_name,
        school_name,
        ok_ell,
        ok_ell_language_code,
        ok_homeless,
        ok_idea,
        ok_primary_disability_code,
        school_address,
        school_id,
        school_zip,
        state_student_number,
        street,
        student_number,
        transfer_comment,
        tps_demographics_lives_with,
        tps_ell_other_lang_spoken,
        tps_service_delivery_code,
        zip,
        '11_12' AS measured_year,
        2011 AS start_year
    FROM
        clean_data.demographics_11_12_pk_k

        UNION ALL

    SELECT 
        city,
        dob,
        entry_code,
        entry_date,
        ethnicity,
        exit_code,
        exit_comment,
        exit_date,
        first_name,
        gender,
        grade_level,
        id,
        last_name,
        lunch_status,
        middle_name,
        school_name,
        ok_ell,
        ok_ell_language_code,
        ok_homeless,
        ok_idea,
        ok_primary_disability_code,
        school_address,
        school_id,
        school_zip,
        state_student_number,
        street,
        student_number,
        transfer_comment,
        tps_demographics_lives_with,
        tps_ell_other_lang_spoken,
        tps_service_delivery_code,
        zip,
        '12_13' AS measured_year,
        2012 AS start_year
    FROM
        clean_data.demographics_12_13_pk_1st

        UNION ALL

    SELECT 
        city,
        dob,
        entry_code,
        entry_date,
        ethnicity,
        exit_code,
        exit_comment,
        exit_date,
        first_name,
        gender,
        grade_level,
        id,
        last_name,
        lunch_status,
        middle_name,
        school_name,
        ok_ell,
        ok_ell_language_code,
        ok_homeless,
        ok_idea,
        ok_primary_disability_code,
        school_address,
        school_id,
        school_zip,
        state_student_number,
        street,
        student_number,
        transfer_comment,
        tps_demographics_lives_with,
        tps_ell_other_lang_spoken,
        tps_service_delivery_code,
        zip,
        '13_14' AS measured_year,
        2013 AS start_year
    FROM
        clean_data.demographics_13_14_pk_2nd

        UNION ALL

    SELECT 
        city,
        dob,
        entry_code,
        entry_date,
        ethnicity,
        exit_code,
        exit_comment,
        exit_date,
        first_name,
        gender,
        grade_level,
        id,
        last_name,
        lunch_status,
        middle_name,
        school_name,
        ok_ell,
        ok_ell_language_code,
        ok_homeless,
        ok_idea,
        ok_primary_disability_code,
        school_address,
        school_id,
        school_zip,
        state_student_number,
        street,
        student_number,
        transfer_comment,
        tps_demographics_lives_with,
        tps_ell_other_lang_spoken,
        tps_service_delivery_code,
        zip,
        '14_15' AS measured_year,
        2014 AS start_year
    FROM
        clean_data.demographics_14_15_pk_3rd

        UNION ALL

    SELECT 
        city,
        dob,
        entry_code,
        entry_date,
        ethnicity,
        exit_code,
        exit_comment,
        exit_date,
        first_name,
        gender,
        grade_level,
        id,
        last_name,
        lunch_status,
        middle_name,
        school_name,
        ok_ell,
        ok_ell_language_code,
        ok_homeless,
        ok_idea,
        ok_primary_disability_code,
        school_address,
        school_id,
        school_zip,
        state_student_number,
        street,
        student_number,
        transfer_comment,
        tps_demographics_lives_with,
        tps_ell_other_lang_spoken,
        tps_service_delivery_code,
        zip,
        '15_16' AS measured_year,
        2015 AS start_year
    FROM
        clean_data.demographics_15_16_pk_4th;
