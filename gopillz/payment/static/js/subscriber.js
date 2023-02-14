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

function validatePhoneNo(no){
    var re = /^\(?(\d{3})\)?(\d{3})?(\d{4})$/;
    if(no.match(re)) {
                return true;
    }
    else {
            var messageData = new Object();
            messageData.status = "danger";
            messageData.message = "Invalid Phone No";
            displayMessage(messageData)
            return false;
    }
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

function savePrescription(){
$('.loader').css('display','block')
    var fileFormData = new FormData();
    var messageData = new Object();
    messageData.status = "danger";

    subscriber_name = document.getElementById('subscriber-name').value
    if (!subscriber_name) {
        messageData.message = "Please Enter Subscriber Name";
        displayMessage(messageData)
        return;
    }
    fileFormData.append('subscriber_name',subscriber_name);

    phone_no = document.getElementById('phone-no').value
    if (!phone_no) {
        messageData.message = "Please Enter Phone No";
        displayMessage(messageData)
        return false;
    }
    fileFormData.append('phone_no',phone_no);
    if (validatePhoneNo(phone_no)==false){
       return false;
    }

    address = document.getElementById('address').value
     if (!address) {
        messageData.message = "Please Enter Address";
        displayMessage(messageData)
        return;
    }
    fileFormData.append('address',address);

    city = document.getElementById('city').value
     if (!city) {
        messageData.message = "Please Enter City";
        displayMessage(messageData)
        return;
    }
    fileFormData.append('city',city);

    var selectedCountry = $('#country option:selected').val()
    if (selectedCountry=='select country') {
        messageData.message = "Please Select Country";
        displayMessage(messageData)
        return;
    }
    fileFormData.append('country',selectedCountry);

    pin_code = document.getElementById('pin-code').value
     if (!pin_code) {
        messageData.message = "Please Enter Pin Code";
        displayMessage(messageData)
        return;
    }
    fileFormData.append('pin_code',pin_code);
    if (validatePinCode(pin_code)==false){
       return false;
    }

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