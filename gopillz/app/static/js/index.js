// slider js

        var index = 0;
        var slides = document.querySelectorAll(".slides");
        var dot = document.querySelectorAll(".dot");
        function changeSlide() {
            if (index < 0) {
                index = slides.length - 1;
            }
            if (index > slides.length - 1) {
                index = 0;
            }
            for (let i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
                dot[i].classList.remove("active");
            }
            if(slides[index]){
               slides[index].style.display = "block";
               dot[index].classList.add("active");
            }
            index++;
            setTimeout(changeSlide, 2000);
        }
        changeSlide();

// accordian js

$('.panel-collapse').on('show.bs.collapse', function () {
    $(this).siblings('.panel-heading').addClass('active');
});
$('.panel-collapse').on('hide.bs.collapse', function () {
    $(this).siblings('.panel-heading').removeClass('active');
});

//browse file js

$(document).ready(function () {
    $('browse__button input').change(function () {
        $('browse__button p').text(this.files.length + " file(s) selected");
    });
});



//animation scroll


 function signupview(){
      window.location.assign("/signup")
    }


    //tabs

        let pillButtonOnText = $('.pill-button-selection_on'),
    pillButtonOffText = $('.pill-button-selection_off'),
    pillButtonHighlight = $('.pill-button-highlight'),
    pillButtonOnTextWidth = pillButtonOnText.outerWidth(),
    pillButtonOffTextWidth = pillButtonOffText.outerWidth(),
    pillButtonOnTextPosition = pillButtonOnText.position(),
    pillButtonOffTextPosition = pillButtonOffText.position(),
    pillButtonInput = $('.pill-button-input');

$('.pillButtonHighlight').css('width', pillButtonOnTextWidth);

$('.pill-button-selection').on('click', function() {
  if(!$(this).hasClass('pill-button-selection_active')) {
    $('.pill-button-selection').removeClass('pill-button-selection_active');
    $(this).addClass('pill-button-selection_active');

    if($(this).hasClass('pill-button-selection_off') && pillButtonInput.prop('checked',true)) {
      pillButtonInput.prop('checked',false);
      pillButtonHighlight.css({
        'width': pillButtonOffTextWidth,
        'left': pillButtonOffTextPosition.left
      });
      console.log("Is Checked - OFF");
    }
    else {
      pillButtonInput.prop('checked',true);
      pillButtonHighlight.css({
        'width': pillButtonOnTextWidth,
        'left': pillButtonOnTextPosition.left
      });
      console.log("Is Checked - ON");
    }
  }
});

if(pillButtonInput.prop('checked',true)) {// default on cold start
  console.log('is checked - cold start');
  pillButtonHighlight.css('width', pillButtonOnTextWidth);
} else {
  console.log('is not checked - cold start');
  pillButtonHighlight.css('width', pillButtonOffTextWidth);
}
