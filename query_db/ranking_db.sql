ALTER DATABASE ranking_test CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

drop table if exists emozioni;
create table emozioni(
    nome_emozione varchar(50) primary key
);

drop table if exists emozioni_img;
create table emozioni_img(
    id_immagine integer references immagine(id_immagine),
    nome_emozione varchar(50) references emozioni(nome_emozione),
    qta integer not null default 1
);

drop table if exists immagini;
create table immagini(
    id_immagine serial primary key,
    id_post integer references post(id_post)
);

drop table if exists post;
create table post(
    id_post serial primary key,
    nome_utente varchar(50) not null,
    data_post datetime not null,
    id_ristorante integer references ristorante(id_ristorante),
    testo varchar(2000) not null,
    punteggio_emoji integer,
    sentiment_comprehend integer,
    negative_comprehend integer,
    positive_comprehend integer,
    neutral_comprehend integer
) DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

drop table if exists ristorante;
create table ristorante(
    id_ristorante serial primary key,
    nome_ristorante varchar(50) not null,
    indirizzo varchar(50) not null,
    telefono varchar(50) not null,
    sito_web varchar(50) not null,
    latitudine decimal(7,4) not null,
    longitudine decimal(7,4) not null,
    categoria varchar(100) not null,
    punteggio_emoji integer,
    punteggio_foto integer,
    punteggio_testo integer
);

drop table if exists tag;
create table tag(
    nome_tag varchar(50) primary key
);

drop table if exists tag_img;
create table tag_img(
    id_immagine integer references immagine(id_immagine),
    nome_tag varchar(50) references tag(nome_tag),
    qta integer
);