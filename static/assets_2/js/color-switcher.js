/* Styles Switcher */

window.console = window.console || (function(){
	var c = {}; c.log = c.warn = c.debug = c.info = c.error = c.time = c.dir = c.profile = c.clear = c.exception = c.trace = c.assert = function(){};
	return c;
})();

jQuery(document).ready(function($) {
	"use strict"

	// Defina as URLs das imagens aqui
    var imageUrls = {
        "assets_2/css/colors/preset.css": "/static/assets/img/go2b-bi-rosa.png",
        "assets_2/css/colors/blue.css": "/static/assets/img/go2b-bi-blue.png",
        "assets_2/css/colors/turquoise.css": "/static/assets/img/go2b-bi-verde.png",
        "assets_2/css/colors/orange.css": "/static/assets/img/go2b-bi.png",
        "assets_2/css/colors/wisteria.css": "/static/assets/img/go2b-bi-roxo.png",
        "assets_2/css/colors/alizarin.css": "/static/assets/img/go2b-bi-vermelho.png",

    };

	var themeColor = localStorage.getItem('themeColor');
	if (themeColor) {
		$("#colors").attr("href", window.STATIC_URL + themeColor);
		$('.brand-logo').attr('src', imageUrls[themeColor]);
	}
	
	function changeColor(colorPath) {
		$("#colors" ).attr("href", window.STATIC_URL + colorPath);
		localStorage.setItem('themeColor', colorPath);
		$('.brand-logo').attr('src', imageUrls[colorPath]);
		return false;
	}

	$("ul.colors .color1" ).click(function(){
		return changeColor("assets_2/css/colors/preset.css");
	});	

	$("ul.colors .color2" ).click(function(){
		return changeColor("assets_2/css/colors/blue.css");
	});	

	$("ul.colors .color3" ).click(function(){
		return changeColor("assets_2/css/colors/turquoise.css");
	});

	$("ul.colors .color4" ).click(function(){
		return changeColor("assets_2/css/colors/orange.css");
	});

	$("ul.colors .color5" ).click(function(){
		return changeColor("assets_2/css/colors/wisteria.css");
	});	

	$("ul.colors .color6" ).click(function(){
		return changeColor("assets_2/css/colors/alizarin.css");
	});

	$("#color-style-switcher .bottom a.settings").click(function(e){
		e.preventDefault();
		var div = $("#color-style-switcher");
		if (div.css("left") === "-145px") {
			$("#color-style-switcher").animate({
				left: "0px"
			}); 
		} else {
			$("#color-style-switcher").animate({
				left: "-145px"
			});
		}
	})

	$("ul.colors li a").click(function(e){
		e.preventDefault();
		$(this).parent().parent().find("a").removeClass("active");
		$(this).addClass("active");
	})

});


//Inject Necessary Styles and HTML
jQuery('head').append('<link rel="stylesheet" id="colors" href="css/colors/preset.css" type="text/css" />');
jQuery('head').append('<link rel="stylesheet" href="css/color-switcher.css" type="text/css" />'); 

jQuery('body').append('' + 
	'<div id="color-style-switcher">' +
		'<div>' + 
			'<h3>Color Palette</h3>' +
			'<ul class="colors">' +
				'<li><a class="color1 active" href="#"></a></li>' +
				'<li><a class="color2" href="#"></a></li>' +
				'<li><a class="color3" href="#"></a></li>' +
				'<li><a class="color4" href="#"></a></li>' +
				'<li><a class="color5" href="#"></a></li>' +
				'<li><a class="color6" href="#"></a></li>' +
			'</ul>' +
		'</div>' +
		'<div class="bottom"> <a href="#" class="settings"><i class="lni-cog"></i></a> </div>' +
	'</div>' +
'');
