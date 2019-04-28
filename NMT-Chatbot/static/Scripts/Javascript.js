//var keyCode = evt ? (evt.which ? evt.which : evt.keyCode) : event.keyCode;

// Check for Enter Key


function asSubmit() {
    var inputVal = document.getElementById("inpTxt").value;
    document.getElementById("txtOut").innerHTML = document.getElementById("txtOut").innerHTML.toString() + "<br/>You: " + inputVal;
    document.getElementById("inpTxt").value = "";
}


$(document).ready(function(){
	var input = document.getElementById("inpTxt");
	input.addEventListener("keyup", function(event){
		if (event.keyCode === 13){
			$('#btnSend').click();
		}
	});
});
$(document).ready(function(){
	$('#btnSend').click(function() {
		$.ajax({
          url: '/SubmitData',
          data: $('#inpTxt').serialize(),
          type: 'GET',
          success: function(response) {			  
              document.getElementById("txtOut").innerHTML = document.getElementById("txtOut").innerHTML.toString() + "<br/>Chat: " + JSON.parse(response);
          },
          error: function(error) {
              console.log(error);
          }
        });
		asSubmit();
    });
});	