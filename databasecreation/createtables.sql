-- SCHEMA: public

-- DROP SCHEMA IF EXISTS public CASCADE;

CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;

create table course (
    course_id serial primary key,
    course_name varchar(256) not null,
    course_number varchar(12) not null,
    course_credits int not null,
    course_grading varchar(64),
    course_restriction varchar(256),
    course_description text,
    course_average_grade float,
    course_grading_chart text,
    course_prerequisites text,
    course_corequisites text,
)

create table professor (
    professor_id serial primary key,
    professor_name varchar(256) not null,
    professor_rating float,
    professor_summary text,
    professor_avg_gpa float,
    professor_grading_chart text,
)

create table section (
    section_id serial primary key,
    course_name varchar(256) not null,
    course_course foreign key references course(course_id),
    professor foreign key references professor(professor_id),
    course_time varchar(256),
    course_seats varchar(256),
    course_summary text,
)