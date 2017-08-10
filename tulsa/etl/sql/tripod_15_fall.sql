-- raw_data.tripod_full_score_15_fall_sheet1
BEGIN;
DROP TABLE IF EXISTS clean_data.tripod_15_fall;
CREATE TABLE clean_data.tripod_15_fall AS
SELECT
    raw."year" AS yr,
    raw.season,
    raw.schoolid_da AS school_id,
    raw.school_name,
    raw.teacherid_da AS teacher_id,
    raw.teacher_first_name || raw.teacher_last_name AS teacher_name,
    raw.class_id,
    CASE raw.grade
        WHEN 'K' THEN 0
        ELSE CAST(raw.grade AS INT)
    END AS grade,
    raw.class_n_student AS responses,
    raw.challenge,
    raw.classroommanagement AS classroom_management,
    raw.captivate,
    raw.care,
    raw.clarify,
    raw.consolidate,
    raw.confer,
    raw.cs
FROM
    raw_data.tripod_full_score_15_fall_sheet1 AS raw;
COMMIT;