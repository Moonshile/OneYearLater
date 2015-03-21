
$(document).ready(function() {
    $('.kinds.sour span').click(choose);
    $('.add-dessert').click(addDessert);
    $('.kinds.dest + button').click(completeChoose);
});

function choose(e) {
    var t = e.target;
    if($(t).hasClass('default')) {
        var colors = ['danger', 'warning', 'success', 'info', 'primary'];
        ($(t).removeClass('default').addClass(colors[Math.floor(Math.random()*colors.length)]));
        var n = t.cloneNode(true);
        $(n).click(function(e) {
            unchoose(e.target.getAttribute('id'));
            btnText();
        });
        $('.kinds.dest').append(n);
    } else {
        unchoose(t.getAttribute('id'));
    }
    btnText();
}

function unchoose(id) {
    var colors = ['danger', 'warning', 'success', 'info', 'primary'];
    $('.kinds.sour #' + id).removeClass(colors.join(' ')).addClass('default');
    $('.kinds.dest #' + id).remove();
}

function btnText() {
    var length = $('.kinds.dest span').length;
    length = length > 2 ? 2 : length;
    var texts = ['随机选择全部', '就选这个活动', '随机选择一项']
    $('.kinds.dest + button').html(texts[length]);
}

function addDessert() {
    // TODO check input and connect to server
    var span = document.createElement('span');
    span.setAttribute('class', 'default');
    span.setAttribute('id', 'ids');//todo
    span.innerHTML = $('#dessert').val();
    $(span).click(choose);
    $('.kinds.sour').append(span);
}

function completeChoose(e) {
    e.target.setAttribute('disabled', 'disabled');
    var colors = ['danger', 'warning', 'success', 'info', 'primary'];
    var length = $('.kinds.dest span').length;
    if(length == 0) {
        var sour = $('.kinds.sour span');
        $('.kinds.dest').append(sour.clone());
        length = sour.length;
    }
    $('.kinds.dest span').removeClass(colors.join(' ')).addClass('default');
    $('.kinds span').unbind('click');
    var res = Math.floor(Math.random()*length);
    $($('.kinds.dest span')[res]).addClass('success');
    //TODO connect to server
}
