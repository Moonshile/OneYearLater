function edit(e) {
    var p = e.target.parentNode;
    try{
        while(p.tagName.toLowerCase() != 'li') {
            p = p.parentNode;
        }
    } catch(e) {
        console.warn(e);
        return;
    }
    p.innerHTML = '\
        <input type="text" value="' + p.textContent.trim() + '">\
        <textarea rows="2" placeholder="具体描述（非必填）"></textarea>\
        <div>\
            <span class="btn btn-xs pull-right btn-cancel" onclick="cancel(' + p.id + ')">\
                <span class="fa fa-chevron-up"></span> 取消\
            </span>\
            <span class="btn btn-xs pull-right" onclick="fix(' + p.id + ',false)">\
                <span class="fa fa-minus-circle text-danger"></span> 搁置\
            </span>\
            <span class="btn btn-xs pull-right" onclick="fix(' + p.id + ',true)">\
                <span class="fa fa-check-circle text-success"></span> 完成\
            </span>\
        </div>';
    p.className = "on";
}

function fix(id, isComplete) {
    var title = $('#' + id + ' input').val();
    var content = $('#' + id + ' textarea').val();
    //TODO
    $('#' + id).html(title + ' <span class="bullet fa fa-' +
     (isComplete ? 'check' : 'minus') +'-square"></span>' +
     '<small>' + content + '</small>');
    $('#' + id).attr('class', 'text-' + (isComplete ? 'success' : 'danger'));
}

function cancel(id) {
    var title = $('#' + id + ' input').val();
    $('#' + id).html('<span>' + title + ' <span class="fa fa-edit"></span></span>');
    $('#' + id).attr('class', '');
    $('#' + id + ' span').click(edit);
}

$(document).ready(function (){
    $('li.todo span').click(edit);
});

