



let current_state = "system";

const source_screens = [
	{ type: "video", source : "sample_video.mp4", state : "WEBCAM_VIDEO", show : true  },
]

function show_screen(com){
	if (com.state == "system"){
		console.log(com.msg);
		return;
	}

	console.log(com.state);

	let video = document.getElementById("screen_WEBCAM_VIDEO");
	if (com.state == "RUNNING"){
		video.play();
	} else {
		video.pause();	
	}
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
  
    let video = document.getElementById("screen_WEBCAM_VIDEO");
    video.loop = true;
    
    $("h1").hide();
  	start_ws(show_screen);

});