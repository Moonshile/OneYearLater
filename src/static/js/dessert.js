
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
    $.ajax({
        url: '/desserts/add/',
        type: 'POST',
        data: {
            'text': $('#dessert').val(),
        },
        success: function(data) {
            if(data.success && data.data) {
                var span = document.createElement('span');
                span.setAttribute('class', 'default');
                span.setAttribute('id', data.data.id);//todo
                span.innerHTML = $('#dessert').val();
                $(span).click(choose);
                $('.kinds.sour').append(span);
                $('#dessert').val('');
            } else if(data.success) {
                $('#dessert').val('');
            } else {
                errs = [];
                for(var i in data.data) {
                    if(typeof(data.data[i]) != 'function') {
                        errs.push(data.data[i].join(','));
                    }
                }
                $('.error.add').html(errs.join(','));
            }
        }
    });
}

function completeChoose(e) {
    var length = $('.kinds.dest span').length;
    if(length == 0) {
        var sour = $('.kinds.sour span');
        $('.kinds.dest').append(sour.clone());
        length = sour.length;
    }
    var res = Math.floor(Math.random()*length);
    $.ajax({
        url: '/desserts/todo/',
        type: 'POST',
        data: {
            'text': $($('.kinds.dest span')[res]).html(),
        },
        success: function(data) {
            if(data.success && data.data) {
                e.target.setAttribute('disabled', 'disabled');
                var colors = ['danger', 'warning', 'success', 'info', 'primary'];
                $('.kinds.dest span').removeClass(colors.join(' ')).addClass('default');
                $('.kinds span').unbind('click');
                $($('.kinds.dest span')[res]).addClass('success');
            } else {
                errs = [];
                for(var i in data.data) {
                    if(typeof(data.data[i]) != 'function') {
                        errs.push(data.data[i].join(','));
                    }
                }
                alert('错误：' + errs.join(','));
            }
        }
    });
}
