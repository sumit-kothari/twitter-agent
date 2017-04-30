

function sendQuery(data) {

	if(data.inputQuery.value) {
		var myKeyVals = {
			query: data.inputQuery.value
		};

		$("#message-list").append('<li class="list-group-item list-group-item-danger">'+ data.inputQuery.value +'</li>');

		$('#myModal').modal('show')

		var saveData = $.ajax({
	      type: 'POST',
	      url: "/api_ai_test",
	      contentType: "application/json",
	      data: JSON.stringify(myKeyVals),
	      dataType: "json"
		});
		
		saveData.error(function() { 
			alert("Something went wrong, please try later"); 
			$('#myModal').modal('hide')
		});

		saveData.success(function(resultData) { 

			$('#myModal').modal('hide')

			console.log(resultData);
			// alert("ok"); 
			$("#message-list").append('<li class="list-group-item list-group-item-success text-right">'+ resultData.message +'</li>');
		});

		data.inputQuery.value = "";

	} else {
		data.inputQuery.value = "";
		alert("Please provide some input query");
	}

	return false;
}