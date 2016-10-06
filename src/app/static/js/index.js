$(document).ready(function(){ 
	$('.info dd').each(function() {
	  $(this).css({width: $(this).text()+'%'});
	});


    setTimeout(function() {
		$('#cover').css({
	    "webkitTransform":"translateX(10%)",
	    "border-color":"#00a7c9",
		});

		$('#calificaciones').css({
	    "webkitTransform":"translateX(80%)",
	    "width": '100%'
		});

		$('#comentar').show( "fast", function() {
		});

		$('#verComentarios').show( "fast", function() {
		});

		$('#camino').show( "fast", function() {
		});

    }, 100);

 })




