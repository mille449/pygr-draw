// annots is an object containing the coordinates for the rectangles and
// text we want to draw on the canvas.  It should already be defined.
function Draw(){

    var canvas = document.getElementById("canvas");
    if (!canvas.getContext) return;

    var ctx = canvas.getContext('2d');

    for each (var r in annots["rectangles"]){
        ctx.fillStyle = r["fill"];
        ctx.fillRect(
            r["rect"][0],
            r["rect"][1],
            r["rect"][2],
            r["rect"][3]
            );

        ctx.strokeStyle = r["outline"];
        ctx.strokeRect(
            r["rect"][0],
            r["rect"][1],
            r["rect"][2],
            r["rect"][3]
            );
    }

    for each (var t in annots["texts"]){
        ctx.fillStyle = t["fill"];
        ctx.fillText(
            t["text"][0],
            t["text"][1],
            t["text"][2]
            );
    }


}


// this is not waiting as intended.  had to put the canvas element before the
// script to make it work
window.onload = Draw;

