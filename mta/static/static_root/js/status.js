

function get_favorites(){
    var $favorites = $('#favorites');
    //console.log('--get_favorites:');
    $favorites.empty();
    //console.log('----emptied!');
    $.ajax({
	url: "favorites/",
        type: "GET",
        data: {},
	
        success: function(results) {
	    console.log('----get_favorites::success!');
	    console.log('results:');
	    console.dir( results );
            $.each(results.favorites, function( i, data ) {
		var favorite = '<div class="favorite-line" data-service="'+data.service+'" data-code="'+data.code+'">'+data.name+': '+data.status+'</div>';
		$favorites.append( favorite );
            });

        },
    });
    
};


$(document).on('click', 'H3', function() {
    get_favorites();
} );



$(document).ready(function() {
    get_favorites();
});

$(document).on('click', '.favorite-line', function(event) {
    event.preventDefault();
    var line = $(this).attr('data-line');
    var id = "#favorite-"+line;
    //var status = $('#'+id).
    //var favorite = '<td><div id="'+id+'" class="favor" data-status="'+status[line].status+'" data-line="' + results.label + '-' + status[line].name + '">on</div></td>';
    $(this).remove();
    $(id).prop('disabled', false);
    $.ajax({
	url: "favorite/remove/",
        type: "GET",
        data: { line: line },
	
        success: function(results) {
	    console.log( 'success' );
        },
    });
    
} );

$(document).on('click', '.favor', function(event) {
    event.preventDefault();

    var service = $(this).attr('data-service');
    var name = $(this).attr('data-name');
    var code = $(this).attr('data-code');
    var status = $(this).attr('data-status');
    $(this).prop('disabled', true);
    console.log( 'adding '+name );
    $.ajax({
	url: "favorite/add/",
        type: "GET",
        data: { service: service, name: name, code: code, status: status },
	
        success: function(results) {
	    console.log( 'added results:' );
            //console.dir( results );
	    $('#favorites').append('<div class="favorite-line" data-service="'+service+'" data-name="'+name+'" data-code="'+code+'" data-status="'+status+'">'+name+' - '+status+'</div>');
	    //get_favorites();
        },
    });
} );


$('#form-check-service').on('submit', function(event){
    //event.defaultPrevent;
    event.preventDefault();

    //console.log("Tearing down Previous");  // sanity check
    //if exists, tear down previous results
    var $res = $('#results');
    $res.empty();
    
    console.log("building");
    //now build backup
    var service = $("#InputService option:selected").text();
    console.log('service:'+service);
    var $h3 = $('<h3></h3>');
    $res.append( $h3.html(service+' querying information now...') );
    console.log('gathering results');
    //console.log("service selected: " + service);
    //console.dir(service);
    //console.log("ajax");
    $.ajax({
	url: "service/status/",
        type: "GET",
        data: { service: service },
	
        success: function(results) {
	    var status = results.status;
            console.log('Successful Ajax Response Started');
	    
	    $res.append( $h3.html(results.label+' Status Updated: '+results.timestamp) );

	    var $statusTable = $('<table class="table table-striped" id="status_table"></table>');
	    $statusTable.append('<tr><th width="80"> Favorite </th><th width="160"> Line Name </th><th> Status </th></tr>');

	    var fav_chk = 'static/img/favorites-add-icon.jpg'

            $.each(status, function( i, line ) {
		console.dir(line)
		var line_id = 'favorite-'+line.code;
		
		var line_img = '<img src="'+fav_chk+'" width="50" height="50" />';
		if (line.is_favorite == 1) {
		    line_img = '';
		    }
		var favorite_div = '<div class="favor" data-name="'+line.name+'" data-status="'+line.status+'" data-code="'+line.code+'" data-service="'+results.label+'">'+line_img+'</div>';
		var favorite_row = '<td><div id="'+line_id+'">'+favorite_div+'</div></td>';
		

		var name = '<td>'+line.name+'</td>';
		var stat = '<div>'+line.status+'</div>';
		if (line.text != "") {
		    stat += '<div>'+line.text+'</div>';
		    }
		stat = '<td>'+stat+'</td>';
		$statusTable.append( '<tr>'+favorite_row+name+stat+'</tr>' );
		
            });
	    $res.append( $statusTable );
            console.log('Successful Ajax Response Ended');
        },
	
	
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
	    console.log('ERROR!!!!!!!');
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
			       " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
		console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    
        
});


