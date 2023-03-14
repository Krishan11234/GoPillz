function displayMessage(data){
    $('.loader').css('display','none')
    $("#message-body").remove();
    $('#django-message').append('<div class="container" id="message-body"><div class="alert alert-dismissible fade show" role="alert"><a></a><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div></div>');
    mainDiv = document.getElementById('message-body'),
    childDiv = mainDiv.getElementsByTagName('div')[0]
    childDiv.classList.add('alert-'+data.status);
    childDiv.getElementsByTagName('a')[0].text = data.message
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function validateEmail(){
    var messageData = new Object();
    adminEmail = document.getElementById("email").value;
    if (!adminEmail) {
        messageData.message = "Please Enter Email Address";
        messageData.status = "danger";
        displayMessage(messageData)
        return false;
    }

    var pattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(!pattern.test(adminEmail)) {
            messageData.message = "Incorrect Email";
            messageData.status = "danger";
            displayMessage(messageData)
            return false
        }
    $("#message-body").remove();
}

function validatePassword(){
    var pw = document.getElementById("pwd").value;
    var Rpw = document.getElementById("rpwd").value;
    var messageData = new Object();

    if (!pw) {
        messageData.message = "**Please Enter Password";
        messageData.status = "danger";
        displayMessage(messageData)
        return false;
    }

    if (!Rpw){
        messageData.message = "**Please Retype Password";
        messageData.status = "danger";
        displayMessage(messageData)
        return false;
    }

    if (pw !=Rpw){
        messageData.message = "**Both the Password must be same";
        messageData.status = "danger";
        displayMessage(messageData)
        return false;
    }
    if (pw.length < 8){
        messageData.message = "**Password length must be atleast 8 characters"
        messageData.status = "danger";
        displayMessage(messageData)
        return false;
    }
    $("#message-body").remove();

}

function validatePinCode(no){
    var re = /^\(?(\d{3})\)?(\d{3})$/;
    if (no.match(re)) {
                return true;
    }
    else {
            var messageData = new Object();
            messageData.status = "danger";
            messageData.message = "Invalid Pin Code";
            displayMessage(messageData)
            return false;
    }
}
function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

function verify_otp(email){
$('.loader').css('display','block')
    var fileFormData = new FormData();
    var messageData = new Object();
    messageData.status = "danger";

    var otp = document.getElementById("otp").value;
    fileFormData.append('otp',otp);
    fileFormData.append('email',email);

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
          type: 'POST',
          url:'/email-verification',
          headers:{
          'X-CSRFToken': csrftoken,
          'contentType': 'application/json',
          },
          contentType: false, //this is requireded please see answers above
          processData: false,
          data:fileFormData,
          success: function(data){
          $('.loader').css('display','none')
            console.log(data)
            if (data.status=='success'){
                window.location.href= 'login-admin';
             }

            $("#message-body").remove();
            $('#django-message').append('<div class="container" id="message-body"><div class="alert alert-dismissible fade show" role="alert"><a></a><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div></div>');
            mainDiv = document.getElementById('message-body'),
            childDiv = mainDiv.getElementsByTagName('div')[0]
            childDiv.classList.add('alert-'+data.status);
            childDiv.getElementsByTagName('a')[0].text = data.message
          },
          error: function(data){
          $('.loader').css('display','none')
          },
      });
}


function send_mail(email){
$('.loader').css('display','block')
    var fileFormData = new FormData();
    var messageData = new Object();
    messageData.status = "danger";

    fileFormData.append('email',email);

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
          type: 'POST',
          url:'/send_mail',
          headers:{
          'X-CSRFToken': csrftoken,
          'contentType': 'application/json',
          },
          contentType: false, //this is requireded please see answers above
          processData: false,
          data:fileFormData,
          success: function(data){
          $('.loader').css('display','none')
          console.log(data)
          if (data.content.message=='success'){
                randString = data.content.rand_string;
                window.location.href= 'email-verification'+'?sample_generator='+randString;
             }
          },
          error: function(data){
          $('.loader').css('display','none')
          },
      });
}


function savePrescription(){
$('.loader').css('display','block')
    var fileFormData = new FormData();
    var messageData = new Object();
    messageData.status = "danger";

    var adminUser = document.getElementById("admin-user-name").value;
    var adminEmail = document.getElementById("email").value;
    var pw = document.getElementById("pwd").value;
    var Rpw = document.getElementById("rpwd").value;

    if (!adminUser) {
        messageData.message = "Please Enter Admin User Name";
        displayMessage(messageData)
        return;
    }
    if (validateEmail()==false){
        return;
    }
    if (validatePassword()==false){
        return;
    }

    fileFormData.append('user_name',adminUser);
    fileFormData.append('email',adminEmail);
    fileFormData.append('password',pw);
    fileFormData.append('retype_password',Rpw);

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
          type: 'POST',
          url:'/prescription',
          headers:{
          'X-CSRFToken': csrftoken,
          'contentType': 'application/json',
          },
          contentType: false, //this is requireded please see answers above
          processData: false,
          data:fileFormData,
          success: function(data){
          $('.loader').css('display','none')
            console.log(data)
            if (data.status=='info'){
                window.location.href= 'verify_email';
             }

            $("#message-body").remove();
            $('#django-message').append('<div class="container" id="message-body"><div class="alert alert-dismissible fade show" role="alert"><a></a><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div></div>');
            mainDiv = document.getElementById('message-body'),
            childDiv = mainDiv.getElementsByTagName('div')[0]
            childDiv.classList.add('alert-'+data.status);
            childDiv.getElementsByTagName('a')[0].text = data.message
            window.scrollTo({ top: 0, behavior: 'smooth' });
          },
          error: function(data){
          $('.loader').css('display','none')
            $("#message-body").remove();
            $('#django-message').append('<div class="container" id="message-body"><div class="alert alert-dismissible fade show" role="alert"><a></a><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div></div>');
            mainDiv = document.getElementById('message-body'),
            childDiv = mainDiv.getElementsByTagName('div')[0]
            childDiv.classList.add('alert-'+data.status);
            childDiv.getElementsByTagName('a')[0].text = data.message
            window.scrollTo({ top: 0, behavior: 'smooth' });
          },
      });
}