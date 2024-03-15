



let current_state = "system";

const source_screens = [
	{ type: "img", source : "01-gira_chiave.png", state : "IDLE", show : true  },
	{ type: "img", source : "02-abilita_pantografo.png", state : "CHIAVE"  },
	{ type: "img", source : "03-attiva_radio.png", state : "PANTOGRAFO"  },
	{ type: "img", source : "04-chiude_porte.png", state : "RADIO"  },
	{ type: "img", source : "05-accendi_qualcosa.png", state : "PORTE"  },
	{ type: "img", source : "06-freno.png", state : "QUALCOSA"  },
	{ type: "img", source : "07-leva.png", state : "ARMED"  },
	{ type: "img", source : "08-avviato.png", state : "RUNNING"  },

]

function show_screen(com){
	if (com.state == "system"){
		console.log(com.msg);
		return;
	}

	let time = (current_state != com.state)? 100: 0; 
	current_state = com.state;

	$("#transition").fadeIn( time, ()=> {
		$("#transition").fadeOut(time*2);
		// Show the screen with id=screen_{comm.state} when the div#transition 
		// is fully shown 

		let screens = $(".backplate")

		let current_screen = $("#screen_" + com.state);
		if (current_screen.length){
			screens.addClass("hidden");
			current_screen.removeClass("hidden")
		} else {
			writeToScreen(" *** Not valid state "+ com.state +" ***")
		}

    if (com.state == 'FINAL'){
      $("#over p").addClass("final");      
    } else {
      $("#over p").removeClass("final");
    }

		$("#over p").text(com.count? com.count : "");
	});
}


$( document ).ready(function() {
    console.log( "ready!" );
    $("#transition").fadeOut(500);
    $("#over p").text("");

    source_screens.forEach( (item) => {
    	let el = document.createElement( item["type"] );
    	if (item["type"] == "video"){
    		let source = document.createElement( "source" );
    		source.setAttribute("src", item["source"]);
    		source.setAttribute("type", "video/mp4");
    		el.append(source);

    	} else if  ((item["type"] == "img")) {
	    	el.setAttribute("src", item["source"]);
    	} else {
    		console.log("not allowed item type" + item["type"]);
    		return;
    	}

    	el.id = "screen_" + item["state"];
    	el.classList.add("backplate");
    	if (!item["show"]) {
	    	el.classList.add("hidden");
    	}
    	$("body").append(el);
    });
    
    $("h1").hide();
  	start_ws(show_screen);

});