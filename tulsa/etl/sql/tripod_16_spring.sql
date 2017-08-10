 -- raw_data.tripod_full_score_16_spring_ee_classlvl
BEGIN;
DROP TABLE IF EXISTS clean_data.tripod_16_spring;
CREATE TABLE clean_data.tripod_16_spring AS
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
    raw."Challenge" AS challenge,
    raw."Classroom Management" AS classroom_management,
    raw."Captivate" AS captivate,
    raw."Care" AS care,
    raw."Clarify" AS clarify,
    raw."Consolidate" AS consolidate,
    raw."Confer" AS confer,
    raw."Composite" AS cs
FROM
    raw_data.tripod_full_score_16_spring_ee_classlvl AS raw;
COMMIT;