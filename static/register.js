// 아이디, 비밀번호 받아 DB에 저장
function yeaaa() {
    console.log("SSDFS")
}
yeaaa()
// $(document).ready(function(){
//     $("form[name=signup_form").submit(function (e) {
//         var $form = $(this);
//         var $error = $form.find(".error");
//         var data = $form.serialize();
    
//         $.ajax({
//             url: "/register",
//             type: "POST",
//             dataType: "json",
//             success: function (res) {
//                 console.log(res);
//                 window.location.href = '/login/'
//             },
//             error: function (res) {
//                 console.log(res);
//                 $error.text(res.responseJSON.msg);
//             },
//         });
    
//         e.preventDefault();
//     });
// })

function sign_up() {
    if (check_dup()) {
        $.ajax({
            type: "POST",
            url: "/register",
            data: {
                id_give: $('#user_id').val(),
                pw_give: $('#password').val(),
                check_pasword: $('#check_password').val()
            },
            success: function (response) {
                console.log(response)
                if (response['result'] == 'success') {
                    console.log(response['result'])
                    alert('회원가입이 완료되었습니다.')
                    $.cookie('mytoken', response['token']);
                    return window.location.replace("/login")
                } else {
                    console.log(response['result'])
                    return alert(response['msg'])
                }
            }
        })
    }
}
function check_dup() {
    let id = $("#user_id").val()
    let password = $("#password").val();
    let passwordConfirm = $("#check_password").val();
    if (id == "") {
        alert("아이디를 입력해주세요")
        $("#user_id").focus()
        return false;
    }
    if (!is_nickname(id)) {
        $("#idHelp").text("아이디의 형식을 확인해주세요. ").removeClass("text-muted").addClass("text-danger");
        $("#user_id").focus()
        return false;
    }
    if (password == "") {
        alert("패스워드를 입력해주세요");
        $("#password").focus()
        return false;
    }
    if (!is_password(password)) {
        $("#passwordHelp").text("패스워드 형식을 확인해주세요. ").removeClass("text-muted").addClass("text-danger");
        $("#password").focus()
        return false;
    }
    if (passwordConfirm == "") {
        alert("패스워드 확인을 입력해주세요");
        $("#check_password").focus()
        return false;
    }
    if (!is_password(passwordConfirm)) {
        $("#passwordConfirmHelp").text("패스워드 형식을 확인해주세요. ").removeClass("text-muted").addClass("text-danger");
        $("#check_password").focus()
        return false;
    }
    return true;
}
function is_nickname(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{3,10}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}