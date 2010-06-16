
// annots is an object containing the coordinates for the rectangles and
// text we want to draw on the canvas.  It should already be defined.
function Draw(){

    var canvas = document.getElementById("canvas");
    if (!canvas.getContext) return;

    var ctx = canvas.getContext('2d');

    for (var r in annots["rectangles"]){
        ctx.fillStyle = annots["rectangles"][r]["fill"];
        ctx.fillRect(
            annots["rectangles"][r]["rect"][0],
            annots["rectangles"][r]["rect"][1],
            annots["rectangles"][r]["rect"][2],
            annots["rectangles"][r]["rect"][3]
            );

        ctx.strokeStyle = annots["rectangles"][r]["outline"];
        ctx.strokeRect(
            annots["rectangles"][r]["rect"][0],
            annots["rectangles"][r]["rect"][1],
            annots["rectangles"][r]["rect"][2],
            annots["rectangles"][r]["rect"][3]
            );
    }

    for (var t in annots["texts"]){
        ctx.fillStyle = annots["texts"][t]["fill"];
        ctx.fillText(
            annots["texts"][t]["text"][0],
            annots["texts"][t]["text"][1],
            annots["texts"][t]["text"][2]
            );
    }

    
}


// this is not waiting as intended.  had to put the canvas element before the
// script to make it work
window.onload = Draw();