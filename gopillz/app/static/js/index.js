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





