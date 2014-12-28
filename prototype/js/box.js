
$(document).ready(function(){
    $(".optional-header").click(function(){
        $(".optional-header .caret").css("transform", $(".optional-body").is(":hidden") ? "rotate(0)" : "rotate(-90deg)");
        $(".optional-body").slideToggle(500);
    })
});
