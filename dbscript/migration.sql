CREATE TABLE sisetu_main (
    nendo     integer not null,
    bunrui    character varying(40),
    dantai_cd character varying(6)  not null,
    tdfk_nm   character varying(40) not null,
    city_nm   character varying(40) not null,
    sheet_nm  character varying(40) not null,
    col_index integer not null,
    col_key1  character varying(40) ,
    col_key2  character varying(40) ,
    col_key3  character varying(40) ,
    col_key4  character varying(40) ,
    col_key5  character varying(40) ,
    col_key6  character varying(40) ,
    col_key7  character varying(40) ,
    col_key8  character varying(40) ,
    col_key9  character varying(40) ,
    col_key10 character varying(40) ,
    col_key11 character varying(40) ,
    col_key12 character varying(40) ,
    tani      character varying(40),
    val_num   bigint,
    val_char  character varying(40),
    val_kba   character varying(40),
    val_kbb   character varying(40),
    val_kbc   character varying(40)
);


ALTER TABLE ONLY sisetu_main
    ADD CONSTRAINT sisetu_main_pkey PRIMARY KEY (
        nendo, 
        dantai_cd,
        sheet_nm,
        col_index
    );


create or replace view V_TDFK as 
select
    substring(dantai_cd,1,2) tdfk_cd,
    tdfk_nm
from
    sisetu_main
group by
    substring(dantai_cd,1,2),
    tdfk_nm
order by
    tdfk_cd
;



drop view V_CITY;
create or replace view V_CITY as 
with nendo as (
    select
        max(nendo) nendo
    from
        sisetu_main
)
select
    substring(a.dantai_cd,1,2) tdfk_cd,
    a.dantai_cd ,
    a.city_nm
from
    sisetu_main a,
    nendo b
where
    a.col_index = 0 and
    a.nendo = b.nendo
group by
    substring(a.dantai_cd,1,2),
    a.dantai_cd,
    a.city_nm
order by
    a.dantai_cd
;


select * from v_city;


