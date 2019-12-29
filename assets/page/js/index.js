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

function formButtonAdd(formname, url_to){
  $('#' + formname).saveStorage();
  window.location.href = url_to + '?return_path=' + window.location.pathname;
}