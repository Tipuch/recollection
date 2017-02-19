/*
* This javascript was hardcoded in order to work
* with this specific formset, may be changed in the future
* depending on the needs
*/

$(function(){
   $('input#button-id-add').click(addForm);
   $('input#button-id-delete').click(removeLastForm);
});

function getLastFormId() {
    let $totalForms = $('input#id_form-TOTAL_FORMS');
    return $totalForms.val() - 1;
}

function addForm() {
    let $lastFormDiv = $("div#div_id_form-"+getLastFormId()+"-word");
    let $lastFormKanjis = $("input#id_form-"+getLastFormId()+"-kanjis");
    let $lastFormOwner = $("input#id_form-"+getLastFormId()+"-owner");
    let $lastFormActions = $('form#id-JpWordFormset div.form-actions');
    $lastFormActions.before($lastFormDiv.clone());
    $lastFormActions.before($lastFormKanjis.clone());
    $lastFormActions.before($lastFormOwner.clone());
    modifyLastForm();
}

function modifyLastForm() {
    let $lastFormDiv = $("div#div_id_form-"+getLastFormId()+"-word:last");
    let $lastFormKanjis = $("input#id_form-"+getLastFormId()+"-kanjis:last");
    let $lastFormOwner = $("input#id_form-"+getLastFormId()+"-owner:last");
    let newId = getLastFormId() + 1;
    $lastFormDiv.attr("id", "div_id_form-"+newId+"-word");
    $lastFormDiv.find("label:first").attr("for", "id_form-"+newId+"-word");
    let $lastFormWord = $lastFormDiv.find("input#id_form-"+getLastFormId()+"-word");
    $lastFormWord.attr("id", "id_form-"+newId+"-word");
    $lastFormWord.attr("name", "form-"+newId+"-word");
    $lastFormKanjis.attr("id", "id_form-"+newId+"-kanjis");
    $lastFormKanjis.attr("name", "form-"+newId+"-kanjis");
    $lastFormOwner.attr("id", "id_form-"+newId+"-owner");
    $lastFormOwner.attr("name", "form-"+newId+"-owner");
    addToTotalForms(1);
}

function removeLastForm() {
    if (getLastFormId() != 0) {
        let $lastFormDiv = $("div#div_id_form-"+getLastFormId()+"-word");
        let $lastFormKanjis = $("input#id_form-"+getLastFormId()+"-kanjis");
        let $lastFormOwner = $("input#id_form-"+getLastFormId()+"-owner");
        $lastFormDiv.remove();
        $lastFormKanjis.remove();
        $lastFormOwner.remove();
        addToTotalForms(-1);
    }
}

function addToTotalForms(number) {
    let $totalForms = $('input#id_form-TOTAL_FORMS');
    $totalForms.val(+($totalForms.val()) + number);
}
