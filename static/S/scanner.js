/*# -*- coding: utf-8 -*-                                                       */
/*#                                                                             */
/*# Created on 2013-10-11                                                       */
/*#                                                                             */
/*# @author: Bartosz Nowak sztosz@gmail.com                                     */
/*#                                                                             */
/*# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007    */

$(document).ready(function() {
    $('form:first *:input[type!=hidden]:first').focus();
});

function commercial_return_close(url) {
    var confirmation = confirm("Are you sure want to delete?");
    if (confirmation) {
        window.location.replace(url);
    }
}
