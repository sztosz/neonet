/**
 * Created by Bartosz on 25.01.14.
 */
$(document).ready(function(){
    $('.confirm').click(function(){
        var answer = confirm("Czy na pewno zamknąć litstę?");
        if (answer){
            return true;
        } else {
            return false;
        }
    });
});
