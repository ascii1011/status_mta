
function row_image(src) {
    return '<img src="'+src+'" width="25" height="25" />';
}

function favorite_row(data) {
    var img = row_image( 'static/img/favorites-remove-icon.jpg' );
    var $fav = $('<button class="btn btn-primary favorite-line" type="submit"></button>');
    $fav.attr('data-name', data.name);
    $fav.attr('data-status', data.status);
    $fav.attr('data-service', data.service);
    $fav.attr('data-code', data.code);
    $fav.append( img );
    $fav.append( data.service+' ['+data.name+'] --- "'+data.status+'"' );

    return $fav;
};

function line_image() {
    var img = row_image( 'static/img/favorites-add-icon.jpg' );
    var $btn = $('<button class="btn btn-primary" type="submit"></button>');

    $btn.append( img );

    return $btn;
}

function line_row(service, data) {

    var $fav = $('<div id="favorite-'+data.code+'" class="favor"></div>');
    $fav.attr('data-name', data.name);
    $fav.attr('data-status', data.status);
    $fav.attr('data-service', service);
    $fav.attr('data-code', data.code);

    if (data.is_favorite == 0) {
	$fav.append( line_image() );
    }

    return $fav;
};


function get_favorites(){
    var $favorites = $('#favorites');
    $favorites.empty();
    $.ajax({
	url: "favorites/",
        type: "GET",
        data: {},
	
        success: function(results) {
            $.each(results.favorites, function( i, data ) {
		favorite = favorite_row( data );
		$favorites.append( favorite );
            });

        },
    });
    
};


$(document).ready(function() {
    get_favorites();
});

$(document).on('click', '.favorite-line', function(event) {
    event.preventDefault();

    var service = $(this).attr('data-service');
    var name = $(this).attr('data-name');
    var code = $(this).attr('data-code');
    var status = $(this).attr('data-status');
    var data = { service: service, name: name, code: code, status: status };

    var id = "#favorite-"+code;
    $(this).remove();
    $.ajax({
	url: "favorite/remove/",
        type: "GET",
        data: data,
	
        success: function(results) {
	    //var $row = line_row( service, data );
	    var $row = line_image();
	    $(id).append( $row );
        },
    });
    
} );

$(document).on('click', '.favor', function(event) {
    event.preventDefault();

    var service = $(this).attr('data-service');
    var name = $(this).attr('data-name');
    var code = $(this).attr('data-code');
    var status = $(this).attr('data-status');
    var data = { service: service, name: name, code: code, status: status };

    $(this).empty();
    $.ajax({
	url: "favorite/add/",
        type: "GET",
        data: data,
	
        success: function(results) {
	    var $row = favorite_row( data );
	    $('#favorites').append( $row );
        },
    });
} );


$('#form-check-service').on('submit', function(event){
    event.preventDefault();

    var $res = $('#results');
    //tear down
    $res.empty();

    //now build backup
    var service = $("#InputService option:selected").text();
    var $h3 = $('<h3></h3>');
    $res.append( $h3.html(service+' querying information now...') );
    $.ajax({
	url: "service/status/",
        type: "GET",
        data: { service: service },
	
        success: function(results) {
	    var status = results.status;
	    
	    $res.append( $h3.html(results.label+' Status Updated: '+results.timestamp) );

	    var $statusTable = $('<table class="table table-striped" id="status_table"></table>');
	    $statusTable.append('<tr><th width="80"> Favorite </th><th width="160"> Line Name </th><th> Status </th></tr>');

	    var fav_chk = 'static/img/favorites-add-icon.jpg'

            $.each(status, function( i, line ) {
		var $row = $('<tr></tr>');

		var $favorite_button = $('<td></td>');
		$favorite_button.append( line_row(results.label, line) );
		$row.append( $favorite_button );

		var name = '<td>'+line.name+'</td>';
		$row.append( name );

		var stat = '<div>'+line.status+'</div>';
		if (line.text != "") {
		    stat += '<div>'+line.text+'</div>';
		    }
		stat = '<td>'+stat+'</td>';
		$row.append( stat );

		$statusTable.append( $row );
		
            });
	    $res.append( $statusTable );
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


