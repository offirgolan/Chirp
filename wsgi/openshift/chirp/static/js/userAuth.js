function submitLoginForm() {
	
	var loginForm = $('#loginForm')
	$.ajax({
	    type: 'POST',
	    url: 'login/',
	    data: loginForm.serialize(),
	    success: function (response) {
	    	if(response.redirect) {
	    		$('#loginModal').modal('hide');
	    		window.location.replace(response.redirect);
	    	}
	        $('#loginFormContainer').html(response);
	    },
	    error: function (response) {
	    }
	 });
	 
	 return false;
}

function submitSignupForm() {
	
	var signupForm = $('#signupForm');
	$.ajax({
	    type: 'POST',
	    url: 'signup/',
	    data: signupForm.serialize(),
	    success: function (response) {
        	if(response.redirect) {
        		$('#signupModal').modal('hide');
        		window.location.replace(response.redirect);
        	}
            $('#signUpFormContainer').html(response);
        },
	    error: function (response) {
	    }
	 });
	 
	 return false;
}