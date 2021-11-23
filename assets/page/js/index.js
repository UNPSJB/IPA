$('.ui.dropdown.top')
  .dropdown({
  	on:'click'
  })
;

$('.ui.dropdown')
  .dropdown({
  	on:'hover'
  })
;

function saveInLocal(formname){
  $('#' + formname).saveStorage();
}

function formButtonAdd(url_to){
  window.location.href = url_to + '?return_path=' + window.location.pathname;
}

$(document).ready(function(){
  if ($('#message_error')[0].childElementCount>0){
    $('.ui.error.message').show();
  }
});