ALTER DATABASE ranking_test CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

drop table if exists emozioni;
create table emozioni(
    nome_emozione varchar(50) not null primary key
);

drop table if exists emozioni_img;
create table emozioni_img(
    id_immagine int not null,
    nome_emozione varchar(50) not null,
    qta integer not null default 1,
    primary key (id_immagine),
    foreign key (id_immagine) references immagine(id_immagine) on delete cascade on update cascade,
    foreign key (nome_emozione) references emozioni(nome_emozione) on delete cascade on update cascade
);

drop table if exists immagini;
create table immagini(
    id_immagine int not null,
    id_post int not null,
    primary key (id_immagine),
    foreign key (id_post) references post(id_post) on delete cascade on update cascade
);

drop table if exists post;
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

drop table if exists ristorante;
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

drop table if exists labels;
create table labels(
    nome_label varchar(50) not null primary key
);

drop table if exists labels_img;
create table labels_img(
    id_immagine int not null,
    nome_label varchar(50) not null,
     primary key(nome_label, id_immagine),
    foreign key (id_immagine) references immagine(id_immagine) on delete cascade on update cascade,
    foreign key (nome_label) references labels(nome_label) on delete cascade on update cascade
);

drop table if exists utente;
create table utente(
    nome_utente varchar(50) not null primary key
);

drop table if exists preferiti;
create table preferiti(
    nome_utente varchar(50) not null,
    id_ristorante int not null,
    primary key (nome_utente),
    foreign key (nome_utente) references utente(nome_utente) on delete cascade on update cascade,
    foreign key (id_ristorante) references ristorante(id_ristorante) on delete cascade on update cascade
);