 "use strict";

  function showInfo(results){
    console.log(results.trail_id)
    
  }

  function getInfo(evt){
    evt.preventDefault();

    let datevalue = $(this).next().val()
    
    var formInputs = {
        "trail_id": $(this).data('tooltip'),
        "date": datevalue,
        "name": $(this).data('name'),
        "url" : $(this).data('url'),
        "length": $(this).data('length'),
        "type" : $(this).data('type'),
        "stars": $(this).data('stars')
    };

    
    $.post("/get-trails-info",formInputs, showInfo);
  }

  $("#hike-it ").on('click', getInfo);
