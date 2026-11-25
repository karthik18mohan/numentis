// Numentis Skills Lab: receives the counselling form and appends a row to the sheet.
// 1) Create a Google Sheet. Row 1 headers: Time | Name | Mobile | You are | Language | Source | Medium | Campaign | Page
// 2) Extensions > Apps Script > paste this file > Save.
// 3) Deploy > New deployment > Web app > Execute as: Me > Who has access: Anyone > Deploy. Copy the Web app URL.
// 4) Put that URL in the form's data-endpoint attribute (build_v2.py DIALOG) and redeploy.
function doPost(e) {
  var d = JSON.parse(e.postData.contents);
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  sh.appendRow([new Date(), d.name, "'" + d.mobile, d.who, d.language, d.source, d.medium, d.campaign, d.page]);
  return ContentService.createTextOutput("ok");
}
