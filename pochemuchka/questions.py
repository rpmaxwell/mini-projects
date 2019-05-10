from wtforms import Form, BooleanField, DateField, StringField, SelectField, PasswordField, IntegerField, validators

question_list = {
	"earnings": [{
		"question_no": 0,
		"questions": [{
			"text": "What's your birthdate?:",
			"validation": [
				{"name": "birthday"},
				{"name": "birthmonth"},
				{"name": "birthyear"}
				]
			},
			{
			"text": "What gender best describes you?",
			"validation": [{"name": "gender"}],
			},
			{
			"text": "What's your marital status?",
			"validation": [{"name": "marital_status"}],
		}]},
		{"question_no": 1,
		"questions": [
			{"text": "how do primarily you make your money?",
			"validation": [{'name': 'income_source'}]},
			{"text": "how much money did you make last year?",
			"validation": [{'name': 'current_salary'}]}
		]
	}]
}