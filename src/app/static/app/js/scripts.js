$(document).ready(function(){
	$('.add_comment').click(function(e){
		$('#frmComment').removeClass('hidden');
		
		return false;
	});
	
	/* Progressive enhancement stuff */
	$('.poll_results').removeClass('hidden');
	$('.ajax_pagination_container').removeClass('hidden');
	$('.social_media_share_widget').removeClass('hidden');
});