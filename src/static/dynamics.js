$(document).ready(function(){
	$('.showlink').click(function(){
		$('body').addClass("loading");
	});
	$('.btn').hover(function(){
			$(this).css('box-shadow', '0 1px 15px rgba(0,0,0,0.6)');
	}, function() {
			$(this).css('box-shadow', '0 0 15px rgba(0,0,0,0.2)');
	});
})