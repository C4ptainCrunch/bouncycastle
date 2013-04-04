$(document).ready(function() {
    function set_form_binding(form) {
        form.on('submit', function() {
            var url = "/add";

            $.ajax({
               type: "POST",
               url: url,
               data: {url :$("#url").val()},
               success: function(data)
               {
                    if (data == null) {
                        show_error('The response from the server was empty :(')
                    }
                    else {
                        if (typeof(data.error) == "undefined") {
                            wait(data);
                        }
                        else {
                            show_error(data.error)
                        }
                    }
               },
               error: function(data)
               {
                    console.error(data);

               }

             });

            return false; // avoid to execute the actual submit of the form.
        });
    }

    function show_error(message) {
        console.error(message);
        alert(message);
    }

    function wait(data) {
        $('#content').empty().html(
            '<h2 class="giga">Please wait, our best monkeys are converting your song</h2>'
            +'<p><img src="http://reflets.info/wp-content/uploads/2012/01/nyan-cat.gif"></p>'
        )
        fetch_status(data.token);
    }

    function fetch_status(token) {
        $.ajax({
            url: "/status?token="+token,
            success: function(data) {
                if (data.status == 'done') {
                    download('/download?token='+data.token)
                    setTimeout(function(){retry(false)},1000)
                }
                else if (data.status == 'error' || typeof(data.error) != "undefined") {
                    if (typeof(data.error) != "undefined") {
                        text = data.error
                    }
                    else {
                        text = 'A wild error appears !'
                    }
                    show_error(text)
                    retry(true)
                }
                else {
                    setTimeout(function(){
                        fetch_status(data.token)
                    }, 10*1000);
                }
            },
        })
    }

    function download(url) {
        var hiddenIFrameID = 'hiddenDownloader',
            iframe = document.getElementById(hiddenIFrameID);

        if (iframe === null) {
            iframe = document.createElement('iframe');
            iframe.id = hiddenIFrameID;
            iframe.style.display = 'none';
            document.body.appendChild(iframe);
        }

        iframe.src = url;
    };

    function retry(error) {
        $.ajax({
            url: "/index_tpl",
            success: function(data) {
                if (error) {
                    text = 'Error, please try again :)'
                }
                else {
                    text = 'Wanna download a new song ?'
                }
                $('#content').empty().html(data)
                $('#form-title').text(text)
                set_form_binding($('#submitform'))
            },
        })
    }

    set_form_binding($('#submitform'))

});