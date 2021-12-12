drop table sisetu_main;

CREATE TABLE sisetu_main (
    nendo     integer not null,
    bunrui    character varying(40),
    daitai_cd character varying(6)  not null,
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
        daitai_cd,
        sheet_nm,
        col_index
    );

 
