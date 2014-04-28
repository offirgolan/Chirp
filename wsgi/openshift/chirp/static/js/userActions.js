var resultCount = 0;
$(document).ready(function() {
    
   setInterval(updateChirps , 10000); // Update every 10 seconds
   setSearchAutocomplete();
   setComposeAutocomplete();
    
});