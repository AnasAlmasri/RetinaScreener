//Django basic setup for accepting ajax requests.
// Cookie obtainer Django
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// Setup ajax connections safetly

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(function() {
    $(document).on("change",".uploadFile", function()
    {
        var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support
        
        if (/^image/.test( files[0].type)){ // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function(){ // set image data as background of div
                //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
                uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url("+this.result+")");  
                $.ajax({
                    url: 'data_ajax_request',
                    data: {
                        'message': 'I want an AJAX response',
                        'img_data': this.result
                    },
                    dataType: 'json',
                    type: 'POST',
                    success: function(data) {
                        if (data.is_valid) {
                            console.log(data.response);
                        } else {
                            console.log("You didn't message : I want an AJAX response");
                        }
                    }
                });
            } 
        }
    });
});

// -----------------------------------------------------------------

// code editor tools
var editor = CodeMirror.fromTextArea(
    document.getElementById('codeeditor'),
    { mode: "python", theme: "monokai", lineNumbers: true, tabSize: 4}
);
editor.setSize("100%", "250");

var terminal = CodeMirror.fromTextArea(
    document.getElementById('terminal'),
    { mode: "shell", theme: "liquibyte", readOnly: true }
);
terminal.setSize("100%", "100");

// Compile and Run button onClick
$(function() {
    $(document).on("click","#btnCompileAndRun", function(){
        console.log("called");
        var source_code = editor.getValue();
        //terminal.getDoc().setValue(text);
        $.ajax({
            url: 'code_editor_ajax_request',
            data: {
                'message': 'compile and run',
                'source_code': source_code
            },
            dataType: 'json',
            type: 'POST',
            success: function(data) {
                console.log(data)
                if (data.is_valid) {
                    terminal.getDoc().setValue(data.response)
                    console.log(data.response);
                } else {
                    console.log("You didn't message : I want an AJAX response");
                }
            }
        });
    });
});

// Compile button onClick
$(function() {
    $(document).on("click","#btnCompile", function(){
        var source_code = editor.getValue();
        //terminal.getDoc().setValue(text);
        $.ajax({
            url: 'code_editor_ajax_request',
            data: {
                'message': 'compile',
                'source_code': source_code
            },
            dataType: 'json',
            type: 'POST',
            success: function(data) {
                if (data.is_valid) {
                    terminal.getDoc().setValue(data.response)
                    console.log(data.response);
                } else {
                    console.log("You didn't message : I want an AJAX response");
                }
            }
        });
    });
});

document.getElementById('activate').addEventListener('click', () => {
    createToast('hello', 'a', 'b');
});


// -------------------------------------------------------------------



    /*
    console.log('called');
    var sourceCode = document.getElementById("codeeditor").value;

    if (sourceCode) {
        document.getElementById("terminal").value = sourceCode;
        //var searchEncoded = encodeURIComponent(search);
    } else {
        console.log("textarea is null");
    }*/





