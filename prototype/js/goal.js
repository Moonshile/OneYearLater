
$(document).ready(function(){
    
    function appendGender(gender) {
        var g = document.getElementById("gender");
        if(g) {
            g.checked = gender;
        } else {
            $(".optional-body").append("<input id='gender' name='gender' type='checkbox' " + (gender ? "checked" : "" ) + " hidden>");
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
                if(d.success) {
                    //todo
                    $(".alert").slideUp();
                } else {
                    var errInfo = {
                        "content": "内容应在1~1000个字符之间", 
                        "email": "需要正确格式的邮件地址",
                        "age": "年龄应不大于128岁",
                        "gender": "亲，不要乱尝试性别哦"
                    };
                    var msg = "";
                    for(e in d.errs) {
                        msg += errInfo[d.errs[e]] + "~";
                    }
                    $(".alert").html(msg).slideDown("fast");
                }
            }
        });
    });
});
