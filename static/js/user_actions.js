 "use strict";

/* Add Comments  */
  function showInfo(results){

    console.log("hi")
  }

  function getInfo(evt){
    evt.preventDefault();

    let inputId = $(this).data("trailId");
    let comments = $(this).prev().val();
    let hikeId = $(this).data("hike-id");

    console.log(comments);

    var formInputs = {
        "trail_id": inputId,
        "comments": comments,
        "hike_id": hikeId
    }
    
    $.post("/add-trails-comment",formInputs, showInfo);

    $(this).attr("class", "btn btn-info btn-sm edit-it")
    $(this).html('<i class="fas fa-pencil-alt"></i>')
    $(this).prev().remove()    
    $(this).before("<span>" +comments+ "</span>&nbsp;&nbsp;")

  }


  /*$(".comment-it").on('click', getInfo);*/
 $(document).on('click', ".comment-it", getInfo)

   /* Now Edit Comments  */
  function showComment(results){
    console.log("hi")
    
  }

  function getComment(evt){
    evt.preventDefault();

    var old_comments = $(this).prev().text();
    console.log($(this).prev());
    // debugger;
    $(this).prev().remove();
    $(this).before("<input type='text'>&nbsp;&nbsp;");
    $(this).prev().val(old_comments);
    $(this).attr("class", "btn btn-info btn-sm comment-it");
    $(this).html("Add");
    var comments = $(this).prev().val()
    console.log(comments)
    let hikeId = $(this).data("hikeId");
    
    var formInputs = {
        "trail_id": $(this).data('trail-id'),
        "comments": comments,
        "hike_id": hikeId
    }


    $.post("/add-trails-comment",formInputs, showComment);


  }

  $(document).on('click', ".edit-it", getComment)


 /* Add Rating */

 function showRating(results){
    console.log("rating print")
 }

 function getRating(evt){
    evt.preventDefault();

    let rating = $(this).prev().val()
    let hikeId = $(this).data("hike-id");

    console.log(rating)

    var formInputs = {
        "u_rating":rating,
        "hike_id": hikeId
    }

    $.post("/add-rating", formInputs, showRating);

    $(this).prev().remove()    
    $(this).before("<span>" +rating+ "</span>")
    $(this).hide();
    $(".rate-it").hide();

 }

 $(".rate-it").on('click', getRating)

