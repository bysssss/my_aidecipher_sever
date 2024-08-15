CREATE TABLE IF NOT EXISTS tb_slide (
    id SERIAL NOT NULL,
    user_id integer NOT NULL,
    slide_name varchar(100),
    image_name varchar(100),
    image_path varchar(100),
    PRIMARY KEY(id)
);
CREATE INDEX idx_tb_slide_user_id ON tb_slide (user_id);

CREATE TABLE IF NOT EXISTS tb_inference (
    id SERIAL NOT NULL,
    user_id integer NOT NULL,
    slide_id integer NOT NULL REFERENCES tb_slide (id),
    decision boolean NOT NULL,
    score float NOT NULL,
    intratumoral_min float,
    intratumoral_avg float,
    intratumoral_max float,
    stromal_min float,
    stromal_avg float,
    stromal_max float,
    error_message text,
    PRIMARY KEY(id)
);
CREATE INDEX idx_tb_inference_user_id ON tb_inference (user_id);
CREATE INDEX idx_tb_inference_slide_id ON tb_inference (slide_id);
