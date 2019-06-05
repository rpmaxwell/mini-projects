function gradeQuiz() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var quizSheet = ss.getSheetByName("quiz");
  var answerSheet = ss.getSheetByName("answer_checker");
  var testing = answerSheet.getRange(11, 6, 1, 1).getValue();
  var allCorrect = true
  for (row_id=0; row_id<6; row_id++) {
    for (col_id=0; col_id<3; col_id++) {
      var submittedAnswer = quizSheet.getRange(row_id+7, col_id+2, 1, 1).getValue();
      var actualAnswer = answerSheet.getRange(row_id+3, col_id+3, 1, 1).getValue();
      if (submittedAnswer == actualAnswer) {
        quizSheet.getRange(row_id+7, col_id+2, 1, 1).setBorder(true, true, true, true, true, true, '#00ff00', SpreadsheetApp.BorderStyle.SOLID)
      }
      else {
        quizSheet.getRange(row_id+7, col_id+2, 1, 1).setBorder(true, true, true, true, true, true, '#ff0000', SpreadsheetApp.BorderStyle.SOLID)
        var allCorrect = false
      }
    }
  }
  if (allCorrect==true) {
    resetQuiz();
    scoreQuiz();
  }
}


function resetQuiz() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var quizSheet = ss.getSheetByName("quiz")
  var answerSheet = ss.getSheetByName("answer_sheet")
  for (row_id=0; row_id<6; row_id++) {
    for (col_id=0; col_id<3; col_id++) {
      quizSheet.getRange(row_id+7, col_id+2, 1, 1).setBorder(false, false, false, false, false, false, '#ffffff', SpreadsheetApp.BorderStyle.SOLID)
      answerSheet.getRange(2, 2, 1, 1).setFormula("=randbetween(3,COUNTA(verbs!A:A)+1)")
      var newVerbId = answerSheet.getRange(2, 2, 1, 1).getValue()
      answerSheet.getRange(2, 2, 1, 1).setValue(newVerbId);
    }
  }
}

function scoreQuiz() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var result_sheet = ss.getSheetByName("mastery");
  var verb_id = answer_sheet.getRange(2, 2, 1, 1).getValue();
  for (var i=3; i<21; i++){
    var current_score = result_sheet.getRange(verb_id, i, 1, 1).getValue();
    result_sheet.getRange(verb_id, i, 1, 1).setValue(current_score+1);
  }
}

