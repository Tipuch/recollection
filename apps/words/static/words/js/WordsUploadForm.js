$(function(){
    $('form#words-upload-form').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        var _self = $(this);
        $.ajax({
            "url": _self.data('action'),
            "data": formData,
            "method": "POST",
            "contentType": false,
            "processData": false,
            "success": showSuccess,
            "error": showErrors
        })
    });

    // add on input change here --> trigger submit for form
});

function showSuccess(data) {
    var message = JSON.parse(data)["message"];
    // inotify here
}

function showErrors(data) {
    var errors = JSON.parse(data);
    // see format of errors and then do something with them
    console.log(errors);
    // inotify the user here of the errors
}
