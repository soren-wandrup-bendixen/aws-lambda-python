create table IRV_SUBJECT_STATE_CHANGES (
    SUBJECTID bigint not null
  , SUBJECTREV bigint not null
  , SUBJECTSTATE integer not null
  , SUBJECTSTATETIME timestamp not null
  , PREVSUBJECTSTATE integer
  , PREVSUBJECTSTATETIME timestamp
  , NEXTSUBJECTSTATE integer
  , NEXTSUBJECTSTATETIME timestamp 
);

alter table IRV_SUBJECT_STATE_CHANGES
  add constraint IRV_SUBJECT_STATE_CHANGES_pk
    primary key ( SUBJECTID, SUBJECTREV )
;


