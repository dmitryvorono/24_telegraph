function show_form(){
  $( "input[name~='header']" ).val($(".b-article__header").html().trim());
  $( "input[name~='signature']" ).val($(".b-article__signature").html().trim());
  $( "textarea[name~='body']" ).val($(".b-article__body").html().trim());
  $( ".js-form" ).removeClass( "js-div-hidden" );
  $( ".b-article" ).addClass( "js-div-hidden" );
}
