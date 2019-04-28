//var keyCode = evt ? (evt.which ? evt.which : evt.keyCode) : event.keyCode;

// Check for Enter Key

function keyEnter()
{
	if(document.layers)
	{
	  document.captureEvents(Event.KEYDOWN);
	}
	
	document.onkeydown = function (evt) {	
	var keyCode = evt ? (evt.which ? evt.which : evt.keyCode) : event.keyCode;
	if(keyCode == 13) {
	    // For Enter.
	  asSubmit();
	}
	
	//if(keyCode == 38){
	// For Up Arrow.
	//	document.getElementById("txtOut").value = inqu;
	//}
	//else
	//{
	//    return true;
	//}
	};
}
function asSubmit() {
    var inputVal = document.getElementById("inpTxt").value;
    document.getElementById("txtOut").innerHTML = document.getElementById("txtOut").innerHTML.toString() + "<br/>You: " + inputVal;
    document.getElementById("inpTxt").value = "";
}