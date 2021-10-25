
function getMousePos(e) {
    //returns mouse x/y coords
    return {x:e.clientX,y:e.clientY};
}


function followedByEric(){
    var imgObj = document.getElementById('ERunicorn');
    var pageWidth = document.body.getBoundingClientRect().width;
    var movingObjectWidth = imgObj.getBoundingClientRect().width;  // width of ER image
    
    imgObj.style.position= 'relative';  // override static default so 'left' can be accessed

    document.onmousemove=function(e) {
        //move ER image left/right to follow mouse
        var mousecoords = getMousePos(e);
    
        // prevent ER image from disappearing off page
        if ((mousecoords.x + movingObjectWidth) < pageWidth) {
            imgObj.style.left = mousecoords.x;
        }
    };
 }
 
 document.addEventListener('DOMContentLoaded', followedByEric);

 
