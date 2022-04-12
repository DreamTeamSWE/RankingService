ALTER DATABASE ranking_test CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
drop table if exists preferito;
drop table if exists emozione_img;
drop table if exists label_img;
drop table if exists immagine;
drop table if exists post;
drop table if exists emozione;
drop table if exists utente;
drop table if exists label;
drop table if exists ristorante;



create table emozione(
    nome_emozione varchar(50) not null primary key
);


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
    punteggio_emoji int null,
    punteggio_foto int null,
    punteggio_testo int null,
    primary key (id_ristorante)
);

create table post(
    id_post int not null,
    nome_utente varchar(50) not null,
    data_post datetime not null,
    id_ristorante int not null,
    testo varchar(2000) not null,
    punteggio_emoji int null,
    score integer not null default 0,
    negative_comprehend int null,
    positive_comprehend int null,
    neutral_comprehend int null,
    primary key (id_post),
    foreign key (id_ristorante) references ristorante(id_ristorante) on delete cascade on update cascade
) DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;


create table immagine(
    id_immagine int not null,
    id_post int not null,
    primary key (id_immagine),
    foreign key (id_post) references post(id_post) on delete cascade on update cascade
);

create table emozione_img(
    id_immagine int not null,
    nome_emozione varchar(50) not null,
    qta int not null default 1,
    primary key (id_immagine),
    foreign key (id_immagine) references immagine(id_immagine) on delete cascade on update cascade,
    foreign key (nome_emozione) references emozione(nome_emozione) on delete cascade on update cascade
);

create table label_img(
    id_immagine int not null,
    nome_label varchar(50) not null,
    primary key(nome_label, id_immagine),
    foreign key (id_immagine) references immagine(id_immagine) on delete cascade on update cascade,
    foreign key (nome_label) references label(nome_label) on delete cascade on update cascade
);

create table preferito(
    nome_utente varchar(50) not null,
    id_ristorante int not null,
    primary key (nome_utente),
    foreign key (nome_utente) references utente(nome_utente) on delete cascade on update cascade,
    foreign key (id_ristorante) references ristorante(id_ristorante) on delete cascade on update cascade
);