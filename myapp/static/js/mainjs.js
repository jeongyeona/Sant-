  document.querySelector("#Username").addEventListener("input", function () {
    this.classList.remove("is-valid");
    this.classList.remove("is-invalid");
    const inputName = this.value;
    const reg = /^([a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]).{1,10}$/;
    if (!reg.test(inputName)) {
      this.classList.add("is-invalid");
      isNameValid = false;
    } else {
      this.classList.add("is-valid");
      isNameValid = true;
    }
  });

  document.querySelector("#Userid").addEventListener("input", function () {
    const self = this;
    self.classList.remove("is-valid");
    self.classList.remove("is-invalid");

    const inputId = this.value;

    const reg = /^[a-z].{4,9}$/;
    if (!reg.test(inputId)) {
      self.classList.add("is-invalid");
      isIdValid = false;
      return;
    } else {
      this.classList.add("is-valid");
      isNameValid = true;
    }
  });



  function checkPwd() {
    document.querySelector("#Userpwd").classList.remove("is-valid");
    document.querySelector("#Userpwd").classList.remove("is-invalid");
    document.querySelector("#Userpwdok").classList.remove("is-valid");
    document.querySelector("#Userpwdok").classList.remove("is-invalid");

    const User_pwd = document.querySelector("#Userpwd").value;
    const User_pwdok = document.querySelector("#Userpwdok").value;
    const reg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&^])[A-Za-z\d@$!%*#?&^]{8,13}$/;
    if (!reg.test(User_pwd)) {
      document.querySelector("#Userpwd").classList.add("is-invalid");
      isPwdValid = false;
      return;
    } else {
      document.querySelector("#Userpwd").classList.add("is-valid");
    }
    // 비밀번호 다르면 발생
    if (User_pwd != User_pwdok) {
      document.querySelector("#Userpwdok").classList.add("is-invalid");
      isPwdValid = false;
    } else {
      document.querySelector("#Userpwdok").classList.add("is-valid");
      isPwdValid = true;
    }
  }

  //비밀번호를 검증하는 함수
  document.querySelector("#Userpwd").addEventListener("input", function () {
    checkPwd();
  });
  document.querySelector("#Userpwdok").addEventListener("input", function () {
    checkPwd();
  });

  document.querySelector("#Useremail").addEventListener("input", function () {
    this.classList.remove("is-valid");
    this.classList.remove("is-invalid");
    //입력한 이메일
    const inputEmail = this.value;
    const reg = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
    if (!reg.test(inputEmail)) {
      this.classList.add("is-invalid");
      isEmailValid = false;
    } else {
      this.classList.add("is-valid");
      isEmailValid = true;
    }
  });

  document.querySelector("#signupForm").addEventListener("submit", function (event) {
    if (document.querySelector("#Username").value === "") {
      event.preventDefault()
      alert('닉네임을 입력해주세요');
    } else if (document.querySelector("#Userid").value === "") {
      event.preventDefault()
      alert('아이디를 입력해주세요');
    } else if (document.querySelector("#Userpwd").value === "") {
      event.preventDefault()
      alert('비밀번호를 입력해주세요');
    } else if (document.querySelector("#Useremail").value === "") {
      event.preventDefault()
      alert('이메일을 입력해주세요');
    }
  });
  
  document.querySelector("#loginform").addEventListener("submit", function (event) {
	    if (document.querySelector("#loginMainForm").value === "") {
	      event.preventDefault()
	      alert('아이디를 입력해주세요');
	    } else if (document.querySelector("#loginpasswordForm").value === "") {
	      event.preventDefault()
	      alert('비밀번호를 입력해주세요');
	    }
	  });
