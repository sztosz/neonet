/**
* Created by Bartosz on 23.10.13.
*/


$(document).ready(function() {
 $('input:text:first').focus();

 $('input:text').bind("keydown", function(e) {
    var n = $("input:text").length;
    if (e.which == 13)
    { //Enter key
      e.preventDefault(); //Skip default behavior of the enter key
      var nextIndex = $('input:text').index(this) + 1;
      if(nextIndex < n)
        $('input:text')[nextIndex].focus();
      else
      {
        $('input:text')[nextIndex-1].blur();
        $('#btnSubmit').click();
      }
    }
  });

  $('#btnSubmit').click(function() {
     alert('Form Submitted');
  });
});
