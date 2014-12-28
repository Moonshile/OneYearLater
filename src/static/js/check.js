
function checkNumber(id) {
    var v = document.getElementById(id).value;
    if(v == "") {
        return true;
    }
    return !isNaN(parseInt(v));
}

function addDanger(id) {
    var p = $("#" + id).parent();
    while(!p.hasClass("form-group")) {
        p = p.parent();
    }
    p.addClass("has-error");
}

function removeFormStates() {
    $(".form-group").removeClass("has-error has-warning has-success");
}

