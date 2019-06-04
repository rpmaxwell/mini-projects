CREATE SCHEMA pochemuchka;
CREATE TABLE pochemuchka.response (
	response_id SERIAL
	,prompt_id INT
	,user_id INT
	,response VARCHAR
	,response_dt TIMESTAMP
);

CREATE TABLE pochemuchka.question (
	question_id SERIAL
	,category_id INT
	,page_id INT
	,question_order_id INT
	,prompt VARCHAR
	,CONSTRAINT unique_question UNIQUE(category_id, page_id, question_order_id)
);

CREATE TABLE pochemuchka.prompt (
	prompt_id SERIAL
	,question_id INT
	,response_type VARCHAR
	,validation VARCHAR
	,placeholder VARCHAR
	,prompt_name VARCHAR
	,CONSTRAINT unique_prompt UNIQUE(question_id, prompt_name)
);

CREATE TABLE pochemuchka.user (
	user_id SERIAL
	,first_name VARCHAR
	,last_name VARCHAR
	,email VARCHAR UNIQUE
	,last_question_id_answered INT
	,signup_dt TIMESTAMP
);