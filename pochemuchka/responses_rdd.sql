CREATE SCHEMA pochemuchka;
CREATE TABLE pochemuchka.responses (
	response_id SERIAL,
	question_id INT,
	subject_id INT,
	user_id INT,
	response VARCHAR,
	response_dt TIMESTAMP,
	CONSTRAINT unique_response UNIQUE(question_id, subject_id, user_id)
);