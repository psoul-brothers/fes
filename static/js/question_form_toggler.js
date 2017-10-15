function event_form_toggler(qestion_type){
    $('#use_question_'+qestion_type).change(function(){
        $('#question_form_'+qestion_type).toggle($(this).is(':checked'));
        $('#edit_question_'+qestion_type).toggle($(this).is(':checked'));
    });
    
    $('#edit_question_'+qestion_type).click(function(){
        $('#question_form_'+qestion_type).show();
    });
}

event_form_toggler('d');
event_form_toggler('l');