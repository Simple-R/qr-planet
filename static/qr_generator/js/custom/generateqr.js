$(document).ready(function(){
    $('#menu button').click(function(){
      var hrefId = $(this).attr('href');
      $('.content .page').hide();
      $('.content').find(hrefId).show();
    });
  });