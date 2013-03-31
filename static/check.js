$(document).ready(function() {
    token  = $('#token').val()
    window.isdown = 0
    window.setInterval(function() {
        $.ajax({
            url: "status?token="+token,
            statusCode: {
                401: function() {
                    alert("An error occured, plz retry\nSubmit your url a second time");
                    window.location.href = "/";
                }
            }
        }).done(function( data ) {
            if (data == 'Done'){
                if (window.isdown == 0) {
                    window.location.href = "/download?token="+token;
                    window.isdown = 1
                }
            }
        })
    }, 10*1000);
});