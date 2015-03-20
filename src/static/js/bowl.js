
$(document).ready(init);

function init() {
    $('li.todo span').click(edit);

    $('.panel-body .fa-check').click(checkTask);
    $('.panel-body .fa-trash').click(delTask);

    $('.edit-task div.item span.content').click(editTaskItem);
    $('.edit-task .text-muted div.item span.btn').click(newTaskItem);
    $('.edit-task div.item span.fa-chevron-up').click(upTaskItem);
    $('.edit-task div.item span.fa-chevron-down').click(downTaskItem);
    $('.edit-task div.item span.fa-trash').click(delTaskItem);

    $('td').click(editTd);
}

function edit(e) {
    e.stopPropagation();
    var p = e.target.parentNode;
    while(p.tagName.toLowerCase() != 'li') {
        p = p.parentNode;
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
    $('li.on textarea').focus().select();
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

function checkTask(e) {
    // TODO connect to server
    $('.panel-primary .hidden').removeClass('hidden');
    $('.panel-primary h3 .fa-check').addClass('hidden');
    $('.panel-primary').removeClass('panel-primary').addClass('panel-default');

    var panel = e.target;
    while(!$(panel).hasClass('panel-default')) {
        panel = panel.parentNode;
    }
    $(panel).removeClass('panel-default').addClass('panel-primary');
    $('.panel-primary .hidden').removeClass('hidden');
    $('.panel-primary .btn-group .fa-check').addClass('hidden');
    $('.panel-primary .btn-group .fa-trash').addClass('hidden');
    // TODO update 碗里的菜菜们
}

function delTask(e) {
    // TODO connect to server
    var col = e.target;
    while(!$(col).hasClass('col-sm-4')) {
        col = col.parentNode;
    }
    col.parentNode.removeChild(col);
}

function editTaskItem(e) {
    var t = e.target;
    var p = t.parentNode;
    var n = document.createElement('input');
    n.setAttribute('type', 'text');
    n.setAttribute('value', t.innerHTML);
    p.replaceChild(n, t);

    $(n).focus().blur(editedTaskItem);
    n.select();
}

function editedTaskItem(e) {
    //TODO connect to server
    var t = e.target;
    var p = t.parentNode;
    var n = document.createElement('span');
    n.setAttribute('class', 'content');
    n.innerHTML = t.value;
    if(t.value) {
        p.replaceChild(n, t);
        $(n).click(editTaskItem);
    } else {
        // remove the task if it is empty
        for(n in p.childNodes) {
            if($(p.childNodes[n]).hasClass('fa-trash')) {
                p.childNodes[n].click();
                break;
            }
        }
    }
}

function newTaskItem(e) {
    var t = e.target;
    while(t.parentNode.tagName.toLowerCase() != 'div'){
        t = t.parentNode;
    }
    var p = t.parentNode;
    var n = document.createElement('input');
    n.setAttribute('type', 'text');
    n.setAttribute('value', '');
    p.replaceChild(n, t);

    $(n).focus().blur(newedTaskItem);
    n.select();
}

function newedTaskItem(e) {
    var t = e.target;
    var p = t.parentNode;
    var n = document.createElement('span');
    n.setAttribute('class', 'btn btn-sm');
    n.innerHTML = '<span class="fa fa-plus"></span> New Task';
    $(n).click(newTaskItem);
    p.replaceChild(n, t);

    if(t.value) {
        //TODO connect to server
        var li = document.createElement('li');
        li.setAttribute('id', 'temp');//TODO
        var div = document.createElement('div');
        div.setAttribute('class', 'item');
        li.appendChild(div);
        var task = document.createElement('span');
        task.setAttribute('class', 'content');
        task.innerHTML = t.value;
        div.appendChild(task);
        var classes = ['fa-trash', 'fa-chevron-down', 'fa-chevron-up'];
        var events = [delTaskItem, downTaskItem, upTaskItem];
        for(var i = 0; i < classes.length; i++) {
            var btn = document.createElement('span');
            btn.setAttribute('class', 'btn btn-sm pull-right fa ' + classes[i]);
            $(btn).click(events[i]);
            div.appendChild(btn);
        }
        var plus_li = n;
        var list = plus_li.parentNode;
        while(list.tagName.toLowerCase() != 'ol') {
            plus_li = plus_li.parentNode;
            list = plus_li.parentNode;
        }
        list.insertBefore(li, plus_li);
    }
}

function upTaskItem(e) {
    //TODO connect to server
    var o = e.target.parentNode.parentNode;
    var s = o.previousSibling;
    // Most browsers will treat blanks or new lines as text nodes
    while(s && s.nodeName.toLowerCase() != 'li') {
        s = s.previousSibling;
    }
    if(s) {
        o.parentNode.insertBefore(o, s);
    }
}

function downTaskItem(e) {
    //TODO connect to server
    var o = e.target.parentNode.parentNode;
    var s = o.nextSibling;
    // Most browsers will treat blanks or new lines as text nodes
    while(s && s.nodeName.toLowerCase() != 'li') {
        s = s.nextSibling;
    }
    if(s && !$(s).hasClass('text-muted')) {
        o.parentNode.insertBefore(s, o);
    }
}

function delTaskItem(e) {
    //TODO connect to server
    var t = e.target.parentNode.parentNode;
    t.parentNode.removeChild(t);
}

function editTd(e) {
    var t = e.target;
    var n = document.createElement('input');
    n.setAttribute('type', 'text');
    n.setAttribute('value', t.innerHTML);
    t.innerHTML = '';
    t.appendChild(n);

    $(n).focus().blur(editedTd);
    n.select();
}

function editedTd(e) {
    var t = e.target;
    var v = t.value;
    t.parentNode.innerHTML = v;
    if(v) {
        //TODO connect to server
    }
}
