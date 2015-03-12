function edit(e) {
    var p = e.target.parentNode;
    p.innerHTML = '\
        <input type="text" value="' + p.textContent.trim() + '">\
        <textarea rows="2" placeholder="具体描述（非必填）"></textarea>\
        <div>\
            <span class="btn btn-xs pull-right btn-cancel" onclick="cancel(' + p.id + ')">\
                <span class="fa fa-chevron-up"></span> 取消\
            </span>\
            <span class="btn btn-xs pull-right" onclick="delay(' + p.id + ')">\
                <span class="fa fa-minus-circle text-danger"></span> 搁置\
            </span>\
            <span class="btn btn-xs pull-right" onclick="complete(' + p.id + ')">\
                <span class="fa fa-check-circle text-success"></span> 完成\
            </span>\
        </div>';
    p.className = "on";
}

function complete(id) {
    var title = $('#' + id + ' input').val();
    var content = $('#' + id + ' textarea').val();
    //TODO
    $('#' + id).html(title + '\
        <span class="bullet fa fa-check-square"></span>\
        <small>' + content + '</small>');
    $('#' + id).attr('class', 'text-success');
}

function delay(id) {
    var title = $('#' + id + ' input').val();
    var content = $('#' + id + ' textarea').val();
    //TODO
    $('#' + id).html(title + '\
        <span class="bullet fa fa-minus-square"></span>\
        <small>' + content + '</small>');
    $('#' + id).attr('class', 'text-danger');
}

function edit(e) {
    var p = e.target.parentNode;
    p.innerHTML = '\
        <input type="text" value="' + p.textContent.trim() + '">\
        <textarea rows="2" placeholder="具体描述（非必填）"></textarea>\
        <div>\
            <span class="btn btn-xs pull-right btn-cancel" onclick="cancel(' + p.id + ')">\
                <span class="fa fa-chevron-up"></span> 取消\
            </span>\
            <span class="btn btn-xs pull-right" onclick="delay(' + p.id + ')">\
                <span class="fa fa-minus-circle text-danger"></span> 搁置\
            </span>\
            <span class="btn btn-xs pull-right" onclick="complete(' + p.id + ')">\
                <span class="fa fa-check-circle text-success"></span> 完成\
            </span>\
        </div>';
    p.className = "on";
}

function cancel(id) {
    var title = $('#' + id + ' input').val();
    $('#' + id).html('<span>' + title + ' <span class="fa fa-edit"></span></span>');
    $('#' + id).attr('class', '');
    $('#' + id + ' > span').click(edit);
}

$(document).ready(function (){
    $('.item ol li[class!="on"] > span').click(edit);
});

