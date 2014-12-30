
$(document).ready(function(){
    
    function appendGender(gender) {
        var g = document.getElementById("gender");
        if(g) {
            g.checked = gender;
        } else {
            $(".optional-body").append("<input id='gender' name='gender' type='checkbox' " + (gender ? "checked" : "" ) + " hidden>");
        }
        if(gender) {
            $("#f").addClass("btn-info");
            $("#m").removeClass("btn-info");
        } else {
            $("#m").addClass("btn-info");
            $("#f").removeClass("btn-info");
        }
    }
    
    var ch1 = "填写你对自己未来一年的要求，我将在明年第一天发邮件提醒你。可以考虑的方面：\n";
    var ch2 = "经济：\n学习：\n健康：";
    $("#content").attr("placeholder", ch1 + ch2).focus(function(){
        $("#content").html(ch2);
    });
    $("#m").click(function() {
        appendGender(false);
    });
    $("#f").click(function() {
        appendGender(true);
    });
    
    $("#submit").click(function(){
        removeFormStates();
        var a = parseInt(document.getElementById("age").value);
        var g = document.getElementById("gender");
        $.ajax({
            url: "add/",
            type: "POST",
            data: {
                "content": document.getElementById("content").value,
                "email": document.getElementById("email").value,
                "age": (isNaN(a) ? null : a),
                "gender": (g ? g.checked : null)
            },
            success: function(data) {
                d = eval(data);
                if(!d.success) {
                    $(".white-form").css("transform", "rotateY(90deg) scale(.8,0.8)");
                    setTimeout('$(".white-form").html($(".submit-success").html()).css("transform", "rotateY(0deg) scale(1,1)")', 500);
                } else {
                    var errInfo = {
                        "content": "内容应在1~1000个字符之间", 
                        "email": "邮件地址需格式正确",
                        "age": "年龄应不大于128岁",
                        "gender": "亲，不要乱尝试性别哦"
                    };
                    var msg = "";
                    for(e in d.errs) {
                        msg += errInfo[d.errs[e]] + "； ";
                        addDanger(d.errs[e]);
                    }
                    if(!checkNumber("age") && d.errs.indexOf("age") == -1) {
                        msg += errInfo["age"] + "； ";
                        addDanger("age");
                    }
                    $(".alert").html(msg).removeClass("alert-success").addClass("alert-danger");
                    if($(".alert").is(":hidden")) {
                        $(".alert").slideDown("fast");
                    }
                }
            }
        });
    });
});
