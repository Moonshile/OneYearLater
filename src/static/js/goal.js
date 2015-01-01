
$(document).ready(function(){
    
    function appendGender(gender) {
        document.getElementById("gender").value = gender ? "2" : "3";
        if(gender) {
            $("#f").addClass("btn-info");
            $("#m").removeClass("btn-info");
        } else {
            $("#m").addClass("btn-info");
            $("#f").removeClass("btn-info");
        }
    }
    
    var ch1 = "填写你对自己未来一年的要求，我将在2016年1月1日发邮件提醒你，看看这一年的梦想是否实现。可以考虑的方面：";
    var ch2 = "经济 学习 健康 ";
    $("#content").attr("placeholder", ch1 + ch2).focus(function(){
        $("#content").html(ch2.replace(/\s+/g, "：\n"));
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
        $.ajax({
            url: "add/",
            type: "POST",
            data: {
                "content": document.getElementById("content").value,
                "email": document.getElementById("email").value,
                "age": (isNaN(a) ? null : a),
                "gender": document.getElementById("gender").value,
            },
            success: function(data) {
                d = eval(data);
                if(d.success) {
                    $(".white-form").css("transform", "rotateY(90deg) scale(.8,0.8)");
                    setTimeout('\
                        $(".goal-id").html(d.data);\
                        $(".before-submit").hide();\
                        $(".submit-success").removeClass("hidden");\
                        $(".white-form").css("transform", "rotateY(0deg) scale(1,1)")\
                    ', 500);
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
