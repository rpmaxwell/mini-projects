function onEdit(e) {
  /*
  @e event object for onEdit simple trigger
  
  Renames the user's ledger sheet if the username on the settings page is edited. If an error 
  is thrown it will attempt to remove spaces special characters and try again.
  */
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = e.range.getSheet()
  if (sheet.getName() == 'Settings') {
      if (e.range.getRow()<4) {
        if (e.range.getColumn()==1) {
          var oldName = sheet.getRange(e.range.getRow(), 5).getValue()
          Logger.log(e.value);
          try {
            ss.getSheetByName(oldName).setName(e.value);
            ss.getSheetByName(sheet.getName()).getRange(e.range.getRow(), 5).setValue(e.value);
          }
          catch(e) {
            var newName = getCleanName(e.value, '');
            ss.getSheetByName(oldName).setName(e.value);
          }
         }
      }
   }
}


function createChargeRow(sheet) {
  /*
  @sheet the sheet on which the new row of the ledger is to be created
  
  Prepopulates and formats the editable ledger row for the given sheet
  */
  var rowFormulas = ['=today()', '', '', '']
  rowFormulas.push('=vlookup(left(E1, len(E1) - len("pays)")),Settings!A2:B3,2,FALSE)')
  rowFormulas = rowFormulas.concat(['=D2*E2','0']);
  sheet.getRange(2, 1, 1, 7).setFormulas([rowFormulas]);
  addValidation(sheet)
  var rowFormats = [ 'YYYY-MM-DD', '@', '@', '$0.00', '0%', '$0.00', '0'];
  sheet.getRange(2, 1, 1, 7).setNumberFormats([rowFormats]);
}

function addValidation(sheet) {
  /*
  @sheet the sheet on which the data validation is to be created
  
  Adds validation by pulling from the "expenses category" of the Settings sheet.
  */
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var settingsSheet = ss.getSheetByName('Settings');
  var validationValues = settingsSheet.getRange(2, 4, settingsSheet.getLastRow(), 1).getValues();
  var validatedCell = sheet.getRange(2, 2);
  var rule = SpreadsheetApp.newDataValidation().requireValueInList(validationValues).build();
  validatedCell.setDataValidation(rule);
}

function newCharge() {
  /*
  Verifies it's being run on the right sheet, creates a new row and moves the rest down
  */
  var ss = SpreadsheetApp.getActiveSpreadsheet()
  var sheet = ss.getActiveSheet()
  var invalidSheets = ['History', 'Settings', 'SettleUp'].filter(function(e){return [sheet.getName()].indexOf(e) === -1});
    Logger.log(invalidSheets)
  if ((invalidSheets.length < 3)) {return;}
  if ((sheet.getRange(2, 4).getValue()=='')||(sheet.getRange(2,4).getValue()==0)) {return;}
  var lastCharge = sheet.getRange(2, 1, 1, 7);
  lastCharge.setValues(lastCharge.getValues());
  sheet.insertRowBefore(2);
  sheet.getRange(2, 1, 1, 7).setBorder(true, null, true, null, null, null, '#000000', SpreadsheetApp.BorderStyle.DASHED);
  sheet.getRange(2, 1, 1, 7).setBackgroundColor('#ffffff');
  sheet.getRange(3, 1, 1, 7).setBorder(null, true, false, true, null, null, '#000000', SpreadsheetApp.BorderStyle.SOLID_THICK);
  sheet.getRange(3, 1, 1, 7).setBackgroundColor('#efefef');
  var createCharge = new createChargeRow(sheet);
  }
  
var getCleanName = function(name, rangeSuffix) {
  /*
   @name the non-standardized name being assinged to the range
   @rangeSuffix the suffix to concatenate to the name portion
   
   pass dynamically created named ranges to this function to validate that it follows at least more of Google's rules for named ranges
   More info can be found here: https://support.google.com/docs/answer/63175
  */
  var regex = /\s\.,*'"`:;\!\?/g;
  var namedRangeName = name.replace(regex, '')
  var namedRange = namedRangeName + rangeSuffix
  return namedRange
}

function settleUp() {
  /*
  
  */
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var users = ss.getSheetByName('Settings').getRange(2, 5, 2, 1).getValues();
  record()
  for (var i=0; i<users.length; i++){
    markAsSettled(users[i][0])
  }
}

function markAsSettled(userName) {
  /*
  For a given user go to the ledger spreadsheet and mark all active charges to 'settled' by assigning the appropriate charge id
  */
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(userName);
  var settledId = ss.getSheetByName('History').getRange(3,1).getValue() + 1;
  Logger.log(settledId)
  for (var i = 3;i<sheet.getLastRow()+1; i++){
    if (sheet.getRange(i,7).getValue() == 0) {
      sheet.getRange(i,7).setValue(settledId)
      sheet.getRange(i, 1, 1, 7).setBackground('#b7b7b7')
    }
    else {
      break
    }
  };
};

function record() {
  /*
  record the final result of the settleUp charge and create a permanent record on the History tab
  */
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('History')
  var settleUpValues = ss.getSheetByName('SettleUp').getRange(4, 5, 1, 4).getValues();
  Logger.log(settleUpValues);
  var historyEntry = [sheet.getRange(3,1).getValue()+1,
                      Utilities.formatDate(new Date(), 'UTC', 'YYYY-MM-dd'),
                      settleUpValues[0][0],
                      settleUpValues[0][2],
                      settleUpValues[0][3]]
  var previousRecords = ss.getRangeByName('settleUpRecords').getValues()
  var historyEntryFormat = ['0', 'YYYY-MM-dd', '@', '@', '$0.00']
  Logger.log(previousRecords);
  Logger.log(sheet.getRange(4, 1, ss.getRangeByName('settleUpRecords').getLastRow()-2, 5));
  sheet.getRange(4, 1, ss.getRangeByName('settleUpRecords').getLastRow()-2, 5).setValues(previousRecords);
  var newEntry = sheet.getRange(3, 1, 1, 5)
  newEntry.setValues([historyEntry])
  newEntry.setNumberFormats([historyEntryFormat])
  newEntry.setBorder(null, null, null, null, false, true, '#000000', SpreadsheetApp.BorderStyle.SOLID)
  ss.setNamedRange('settleUpRecords', sheet.getRange(3, 1, ss.getRangeByName('settleUpRecords').getLastRow()-1, 5));
  ss.getRangeByName('settleUpRecords').setBorder(true, true, true, true, false, null, '#000000', SpreadsheetApp.BorderStyle.SOLID_THICK)
}

