ALTER DATABASE ranking_test CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
drop table if exists preferito;
drop table if exists emozione_img;
drop table if exists label_img;
drop table if exists immagine;
drop table if exists post;
drop table if exists utente;
drop table if exists label;
drop table if exists ristorante;
drop table if exists confidenza_emozioni;
drop table if exists analisi_testo;

/*
delete from preferito;
delete from emozione_img;
delete from label_img;
delete from immagine;
delete from post;
delete from utente;
delete from label;
delete from ristorante;
delete from confidenza_emozioni;
delete from analisi_testo;

select * from preferito;
select * from emozione_img;
select * from label_img;
select * from immagine;
select * from post;
delete from emozione;
select * from utente;
select * from label;
select * from ristorante;
*/


create table utente(
    nome_utente varchar(50) not null primary key
);

create table label(
    nome_label varchar(50) not null primary key
);

create table ristorante(
    id_ristorante int not null,
    nome_ristorante varchar(50) not null,
    indirizzo varchar(50) null,
    telefono varchar(50) null,
    sito_web varchar(50) null,
    latitudine decimal(7,4) not null,
    longitudine decimal(7,4) not null,
    categoria varchar(100) not null,
    punteggio_emoji float null,
    punteggio_foto float null,
    punteggio_testo float null,
    primary key (id_ristorante)
);

create table post(
    id_post varchar(50) not null,
    nome_utente varchar(50) not null,
    data_post datetime not null,
    id_ristorante int not null,
    testo varchar(3000) null,
    punteggio_emoji float null,
    punteggio_testo float null,
    punteggio_foto float null,
    primary key (id_post),
    foreign key (id_ristorante) references ristorante(id_ristorante) on delete cascade on update cascade

) DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

create table analisi_testo(
    id_post varchar(50) not null,
    negative_comprehend float not null,
    positive_comprehend float not null,
    neutral_comprehend float not null,
    mixed_comprehend float not null,
    primary key (id_post),
    foreign key (id_post) references post(id_post) on delete cascade on update cascade
);

create table immagine(
    id_immagine int not null,
    id_post varchar(50) not null,
    primary key (id_immagine),
    foreign key (id_post) references post(id_post) on delete cascade on update cascade
);

create table emozione_img(
    id_immagine int not null,
    nome_emozione varchar(50) not null,
    qta int not null,
    primary key (id_immagine, nome_emozione),
    foreign key (id_immagine) references immagine(id_immagine) on delete cascade on update cascade,
    check (nome_emozione in ('HAPPY', 'CALM', 'SAD', 'ANGRY', 'SURPRISED', 'CONFUSED', 'DISGUSTED'))
);

create table label_img(
    id_immagine int not null,
    nome_label varchar(50) not null,
    /*confidenza double not null,*/
    primary key(nome_label, id_immagine),
    foreign key (id_immagine) references immagine(id_immagine) on delete cascade on update cascade,
    foreign key (nome_label) references label(nome_label) on delete cascade on update cascade
);

create table preferito(
    nome_utente varchar(50) not null,
    id_ristorante int not null,
    primary key (nome_utente, id_ristorante),
    foreign key (nome_utente) references utente(nome_utente) on delete cascade on update cascade,
    foreign key (id_ristorante) references ristorante(id_ristorante) on delete cascade on update cascade
);

create table confidenza_emozioni(
    happy float not null,
    calm float not null,
    sad float not null,
    angry float not null,
    surprised float not null,
    confused float not null,
    disgusted float not null,
    num_persona int not null,
    id_immagine int not null,
    primary key (num_persona, id_immagine),
    foreign key (id_immagine) references immagine(id_immagine) on delete cascade on update cascade
);