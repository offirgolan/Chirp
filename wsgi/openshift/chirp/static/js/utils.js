function updateChirps() {
	
	$.ajax({
        type: 'get',
        url: 'updateChirps/',
        success: function (response) {
            $('#chirpListContainer').html(response);
            updateUserData();
        },
        error: function (response) {
        }
     })
	
}

function composeChirp() {
	
	var composeChirpForm = $('#composeChirpForm');
	$.ajax({
	    type: 'POST',
	    url: '/compose/',
	    data: composeChirpForm.serialize(),
	    success: function (response) {
            $('#composeChirpContainer').html(response);
            updateChirps();
            // Reset autocomplete options on form refresh
            setComposeAutocomplete();
        },
	    error: function (response) {
	    }
	 });
	 
	 return false;
}

function submitUpdateProfileForm() {
	
	// Since we need to send a file, using FormData puts the file data in request.FILE
	var updateProfileForm = $('#updateProfileForm');
	var formData = new FormData($('#updateProfileForm')[0]);
	formData.append('profile_pic', updateProfileForm.find('input[name="profile_pic"]').val());
	$.ajax({
	    type: 'POST',
	    url: '/updateProfile/',
	    data: formData,
	    processData: false,
		contentType: false,
	    success: function (response) {
            $('#updateProfileFormContainer').html(response);
            // Update dashboard profile picture to the new one to avoid the need of a manual page refresh
            $('#dashProfilePicture').attr('src', $('#updateProfilePicture').attr('src'))
        },
	    error: function (response) {
	    	console.log(response);
	    }
	 }); 
	 
	 return false;
}

function submitSearchForm() {
	
	if(resultCount == 0)
		return false;
	
	var searchForm = $('#searchForm');
	var data = {'query': $('#search').val()};
	$.ajax({
	    type: 'get',
	    url: '/search/',
	    data: data,
	    success: function (response) {
            if(response.redirect) {
        		window.location.replace(response.redirect);
        	}
        },
	    error: function (response) {
	    }
	 });
	 
	 return false;
}

function setSearchAutocomplete() {
	$("#search").autocomplete({
	    source: "/autoCompleteSearch/",
	    minLength: 2,
	    select: function(event, ui) {
	         $('#search').val(ui.item.value);
	         $('#searchForm').submit();  
	    },
	    response: function(event, ui) {
            resultCount = ui.content.length;
        }
   });

}

function setComposeAutocomplete() {
	var currDelimiter;
	
	
	// Function for multiword autocomplete
	function split( val ) {
			return val.split( /(@|#)\s*/ );
	}
	function extractLast( term ) {
			query = split(term);
			word = query.pop();
			delimiter = query.pop();
			currDelimiter = delimiter;
			return delimiter + word;
	}
	
	// Disable compose on enter
	$("#id_message").keypress(function(e) {
	    var code = (e.keyCode ? e.keyCode : e.which);
	    if(code == 13) { //Enter keycode
	        return false;
	    }
	});
	
	$('#id_message').focus(function()
	{
	    /*to make this flexible, I'm storing the current width in an attribute*/
	    $(this).attr('data-default-height', '42px');
	    $(this).attr('data-default-placeholder', $(this).attr('placeholder'));
	    $(this).attr('placeholder', '');
	    $(this).animate({ height: 80 }, 'fast');
	}).blur(function()
	{
	    /* lookup the original width */
	    var h = $(this).attr('data-default-height');
	    $(this).animate({ height: h }, 'fast');
	    $(this).attr('placeholder', $(this).attr('data-default-placeholder'));
	});
	
	// Set the options with a custom ajax call
	$("#id_message").autocomplete({
	    //source: "/autoCompleteSearch/",
	    source: function( request, response ) {
			  // delegate back to autocomplete, but extract the last term
			   $.ajax({
	              url: '/autoCompleteSearch/',
				  data :  {'term' : extractLast( request.term ) },
	              dataType: "json",
	              type: "GET",
	              success: function (data) {
	                    response($.map(data, function(item) {
	                    	return item;
						}));
	              }
              });
		},
	    minLength: 2,
	    focus: function(event, ui) {
	    	 // Replace the value that was typed with the full value selected
	    	 currMessage = $('#id_message').val();
	    	 message = currMessage.substring(0, currMessage.lastIndexOf(currDelimiter));
	         $('#id_message').val(message + ui.item.value);	         
	         return false;
	    },
	    select: function(event, ui) {
	         currMessage = $('#id_message').val();
	    	 message = currMessage.substring(0, currMessage.lastIndexOf(currDelimiter));
	         $('#id_message').val(message + ui.item.value);	 
	         
	         return false;
	    },
	    response: function(event, ui) {
            //resultCount = ui.content.length;
        }
   });

}

function updateUserData() {
	
	$.ajax({
        type: 'get',
        url: 'updateUserData/',
        success: function (response) {
            $('#userData').html(response);
        },
        error: function (response) {
        }
     })
	
}