

function choose(id) {
    $(".ans-list p").css("color", "#888");
    $(".ans-list p .glyphicon").removeClass("glyphicon-ok");
    $(".ans" + id).css("color", "#ccc");
    $(".ans" + id + " .glyphicon").addClass("glyphicon-ok");
    $("#choosen").attr("value", id);
}

function colorPercent(percent) {
    var red = percent > .5 ? 153*(1 - percent)*2 : 153;
    var green = percent > .5 ? 153 : 153*percent*2;
    return "#" + (((red<<8)|green)<<8).toString(16);
}

function timer_start(e, t, i, callback) {
    old_t = t;
    var timer = setInterval(function(){
        e.html(parseInt(t/1000) + "." + ((t%1000)/100) + "s");
        e.css("color", colorPercent(t/old_t));
        t = t - i;
        if(t < 0) {
            clearInterval(timer);
            callback();
        }
    }, i);
}

$(document).ready(function(){
    timer_start($(".timer"), 10000, 100, function(){
        var te = $(".timer");
        var count = 3;
        var warn_timer = setInterval(function(){
            te.animate({fontSize: "25px"}, "fast");
            te.animate({fontSize: "20px"}, "fast");
            count--;
            if(count <= 0) {
                clearInterval(warn_timer);
            }
        }, 1000);
    });
});
