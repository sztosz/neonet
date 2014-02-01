/*# -*- coding: utf-8 -*-                                                       */
/*#                                                                             */
/*# Created on 2013-10-11                                                       */
/*#                                                                             */
/*# @author: Bartosz Nowak sztosz@gmail.com                                     */
/*#                                                                             */
/*# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007    */


$(document).ready(function() {
 $('input:text:first').focus();

 $('input:text').bind("keydown", function(e) {
    var n = $("input:text").length;
    if (e.which == 13)
    { //Enter key
      e.preventDefault(); //Skip default behavior of the enter key
      var nextIndex = n.index(this) + 1;
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

function commercial_return_close(url) {
    var confirmation = confirm("Are you sure want to delete?");
    if (confirmation) {
        window.location.replace(url);
    }
}
