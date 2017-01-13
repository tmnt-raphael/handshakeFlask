$(".upvoteButton").click(function(){

  var alarmId = jQuery(this).prop('id');

  $.ajax({
    url: '/upvote/',
    type: 'PUT',
    data: "alarmId=" + alarmId
  });

  console.log("upvoted");
  console.log(alarmId);

});