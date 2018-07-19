function checkPass ()
{
    with (document)
    if (getElementById ('password').value != getElementById ('confirm_password').value) {
        document.getElementById("confirm_password").className = "invalid";
    }
    else{
        document.getElementById("confirm_password").className = "validate";
    }
}

$(document).ready(function() {
    $('select').material_select();
});

$(function(){
	'use strict';

	var regexes = {
		last_name: 	/^[а-яА-ЯёЁ]+$/,
		first_name: /^[а-яА-ЯёЁ]+$/,
	};

	$.each($('input:not([type="submit"])'), function() {
		$(this).on('focusout', function(){
			if(!regexes[$(this).attr('id')].test($(this).val())){
        $(this).removeClass('valid');
        $(this).addClass('invalid');
			} else {
        $(this).removeClass('invalid');
				$(this).addClass('valid');
			}
		});
	});
});