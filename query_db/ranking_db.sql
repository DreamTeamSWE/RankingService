drop table if exists emozioni;
create table emozioni(
    nome_emozione varchar(50) primary key
);

drop table if exists emozioni_img;
create table emozioni_img(
    id_immagine integer references immagine(id_immagine),
    nome_emozione varchar(50) references emozioni(nome_emozione),
    qta integer
);

drop table if exists immagine;
create table immagine(
    id_immagine serial primary key,
    id_post integer references post(id_post)
);

drop table if exists post;
create table post(
    id_post serial primary key,
    id_ristorante integer references ristorante(id_ristorante),
    punteggio_emoji integer,
    sentiment_comprehend integer,
    negative_comprehend integer,
    positive_comprehend integer,
    neutral_comprehend integer
);

drop table if exists ristorante;
create table ristorante(
    id_ristorante serial primary key,
    nome_ristorante varchar(50),
    indirizzo varchar(50),
    citta varchar(50),
    provincia varchar(50),
    telefono varchar(50),
    sito_web varchar(50),
    orario_apertura varchar(50),
    orario_chiusura varchar(50),
    latitudine varchar(50),
    longitudine varchar(50),
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