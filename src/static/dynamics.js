$(document).ready(function(){
	$('.showlink').click(function(){
		$('body').addClass("loading");
	});
	$('.btn').hover(function(){
			$(this).css('box-shadow', '0 1px 15px rgba(0,0,0,0.6)');
	}, function() {
			$(this).css('box-shadow', '0 0 15px rgba(0,0,0,0.2)');
	});

	let genBoxes = $('.genBoxSmall');
	let last_was_floated = false;
	for (let j=0; j<genBoxes.length; j++){	
		if ( !last_was_floated ) {
			genBoxes[j].className += ' right';
		}
		if ( j % 2 == 0 ){
			last_was_floated = true;
			continue;
		}
		last_was_floated = false;
	}
})