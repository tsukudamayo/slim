CREATE TABLE ingredient_name_map
(
    name_id int4 NOT NULL,
    ingredient_id int4 NOT NULL,
    search_key VARCHAR NOT NULL,
    ingredient_kana VARCHAR NOT NULL,
    PRIMARY KEY(name_id)
);
