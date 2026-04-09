create database if not exists loja;

use loja;

create table produto(
    id int auto_increment primary key,
    nome varchar(60) not null,
    descricao varchar(150) not null,
    qntd_disponivel int not null default 0,
    preco decimal(10,2) not null
);

create table venda (
    id int auto_increment primary key,
    id_produto int not null,
    foreign key (id_produto) references produto (id) on delete restrict,
    qntd_vendida decimal(10,2) not null,
    data_venda date
);