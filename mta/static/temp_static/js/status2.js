
$('#form-check-service').on('submit', function(event){
    //event.defaultPrevent;
    event.preventDefault();

    console.log("Tearing down Previous");  // sanity check
    //if exists, tear down previous results
    var $res = $('#results');
    $res.empty();
    
    console.log("building");
    //now build backup
    var service = $("#InputService option:selected").text();
    var $h3 = $('<h3></h3>');
    $res.append( $h3.html(service+' querying information now...') );

    //console.log("service selected: " + service);
    //console.dir(service);
    console.log("ajax");
    $.ajax({
	url: "status/",
        type: "GET",
        data: { service: service },
	
        success: function(results) {
	    var status = results.status;
            console.log('Successful Ajax Response Started');
	    
	    $res.append( $h3.html(results.label+' Status Updated: '+results.timestamp) );

	    var $statusTable = $('<table class="table table-striped" id="status_table"></table>');
	    $statusTable.append('<tr><th width="160"> Line Name </th><th> Status </th></tr>');

            $.each(status, function( line ) {
		console.log('line:' +status[line].name);
		var name = '<tr><td>'+status[line].name+'</td>';
		var stat = '<div>'+status[line].status+'</div>';
		if (status[line].text != "") {
		    stat += '<div>'+status[line].text+'</div>';
		    }
		stat = '<td>'+stat+'</td></tr>';
		$statusTable.append( name+stat );
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
