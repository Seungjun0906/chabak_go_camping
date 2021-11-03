function sign_in() {
    // 아이디, 비밀번호 값을 변수에 담는다.
    let user_id = $("#user_id").val()
    let password = $("#password").val()
    // 아이디를 입력하지 않았다면 "아이디를 입력해주세요."라는 경고 메세지가 나오면서 인풋 박스에 포커스하고 함수 종료
    if (user_id == "") {
        alert("아이디를 입력해주세요.")
        $("#user_id").text("아이디를 입력해주세요.")
        $("#user_id").focus()
        return false;
    }
    if (password == "") {
        alert("비밀번호를 입력해주세요")
        $("#password").text("비밀번호를 입력해주세요.")
        $("#password").focus()
        return false;
    } 
    //ajax로 post방식을 통해 sign_in에 아이디와 비밀번호를 보냄
    $.ajax({
        type: "POST",
        url: "/login",
        data: {
            user_id: user_id,
            password: password
        },
        success: function (response) {
            // 결과값이 success라면
            if (response['result'] == 'success') {
                //쿠키생성, 메세지
                console.log(response['result'])
                $.cookie('mytoken', response['token'])
                window.location.href='/article';
                alert('로그인완료!');
            } else {
                alert(response['msg'])
            }
        }
    });
}