window.onload = (function (window){
    $('.job').each(
        function () {
            var prog_bar = $(this).find('.progress');
            var progress = $(this).attr('progress');
            prog_bar.css('width', progress+'%');
            if(progress > 80) {
                prog_bar.addClass('red');
            } else if(progress > 70) {
                prog_bar.addClass('yellow');
            } else {
                prog_bar.addClass('green');
            }

        }
    );

});
