function showhide(showhide_id) {
	if(document.getElementById('checkbox_'+showhide_id).checked) {
		document.getElementById(showhide_id).style.visibility = 'visible';
	}
 		else {
		document.getElementById(showhide_id).style.visibility = 'hidden';
	}
}
