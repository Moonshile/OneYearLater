

$(document).ready(function() {
    var data = [];
    var len = 100;
    for(var i = 1; i <= len; i++) {
        data.push({'proportion': i/len});
    }
    historyHorizontal($('.history-h'), data);
});