-- SCHEMA: public

DROP SCHEMA IF EXISTS public CASCADE;

CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;

CREATE TABLE course (
    course_id serial primary key,
    course_name varchar(256) NOT NULL,
    course_number varchar(12) NOT NULL,
    course_credits int NOT NULL,
    course_grading varchar(64),
    course_restriction varchar(256),
    course_description text,
    course_average_grade float,
    course_grading_chart text,
    course_prerequisites text,
    course_corequisites text
);

CREATE TABLE professor (
    professor_id serial primary key,
    professor_name varchar(256) NOT NULL,
    professor_rating float,
    professor_summary text,
    professor_avg_gpa float,
    professor_grading_chart text
);

CREATE TABLE section (
    section_id serial primary key,
    course_name varchar(256) NOT NULL,
    course_id int REFERENCES course(course_id),
    professor_name varchar(256) NOT NULL,
    professor_rating float,
    course_time varchar(256),
    course_total_seats int,
    course_open_seats int,
    course_waitlist int,
    course_summary text,
    course_rating float
);