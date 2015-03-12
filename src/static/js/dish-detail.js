function complete(id) {
    var title = $('#' + id + ' input').val();
    var content = $('#' + id + ' textarea').val();
    //TODO
}

function cancel(id) {
    var title = $('#' + id + ' input').val();
    var content = $('#' + id + ' textarea').val();
    //TODO
}

$(document).ready(function (){
    $('.item ol li[class!="on"] > span').click(function(e) {
        var p = e.target.parentNode;
        p.innerHTML = '\
<input type="text" value="' + p.textContent.trim() + '">\
<textarea rows="2" placeholder="具体描述（非必填）"></textarea>\
<div>\
    <span class="btn btn-xs pull-right" onclick="complete(' + p.id + ')">\
        <span class="fa fa-check-circle text-success"></span> 完成\
    </span>\
    <span class="btn btn-xs pull-right" onclick="cancel(' + p.id + ')">\
        <span class="fa fa-minus-circle text-danger"></span> 搁置\
    </span>\
</div>';
        p.className = "on";
    });
});

