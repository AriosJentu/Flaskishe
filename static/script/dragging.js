//dragElement(document.getElementById("divdrg"))

var elements = document.getElementsByClassName("divDragger")

for (var element of elements) {
	dragElement(element);
}

var curX = null, curY = null;
document.addEventListener('mousemove', onMouseUpdate, false);
document.addEventListener('mouseenter', onMouseUpdate, false);

var spt = document.getElementById("titledebug"); 
var flaskEditor = document.getElementById("DatabaseEditor");

function onMouseUpdate(e) {
	curX = e.pageX;
	curY = e.pageY;
}

function dragElement(elemnt) {

	var pos1 = 0, pos2 = 0;
	var width = null, height = null;
	var isMouseDown = false
	var curXprev = 0, curYprev = 0;
	var moveFrom = 0, moveTo = 0;

	elemnt.onmousedown = dragMouseDown;
	elemnt.onmouseover = mouseOver;
	elemnt.onmouseout = mouseOut;

	var div_elements = document.getElementsByClassName("divElements");
	var div_element = null;
	var div_redblock = null;

	var div_parent = null;


	for (var div_el of div_elements) {
		if (div_el.getAttribute("name") === elemnt.getAttribute("name")) {

			if (div_el.getAttribute("id") === "divRedBlock") {

				div_redblock = div_el;

			} else {

				div_element = div_el;
			}
		}
	}

	var div_drag_blocks = document.getElementsByClassName("divDrag");
	var div_dragger = null;

	var ceils = document.getElementsByClassName("divTableCell")

	for (var div_drg of div_drag_blocks) {
		if (div_drg.getAttribute("name") === elemnt.getAttribute("name")) {
			div_dragger = div_drg;
			div_parent = div_drg.parentNode.parentNode
		}
	}

	function mouseOver(el) {
		if (!isMouseDown) {

			elemnt.style["background-color"] = "#9EEE9E";
		}
	}

	function mouseOut(el) {
		if (!isMouseDown) {

			elemnt.style["background-color"] = "#EEEEEE";
		}
	}


	function dragMouseDown(el) {
	
		
		el = el || window.event;

		width = elemnt.offsetWidth;
		height = element.offsetHeight;

		curXprev = curX;
		curYprev = curY;

		isMouseDown = true;

		
		elemnt.style.position = "absolute";
		elemnt.style.border = "1px solid black";
		elemnt.style["background-color"] = "#FFD9CC";

		if (div_dragger !== null) {
			div_dragger.style.border = "0px solid black";
		}

		if (div_element !== null) {

			div_element.style.display = "none";
		}
		if (div_redblock !== null) {

			div_redblock.style.display = "block";
			div_redblock.style.width = width+"px";
			div_redblock.style.height = width+"px";
		}

		elemnt.style.width = width+"px";
		elemnt.style.height = height+"px";

		elemnt.style.left = elemnt.offsetLeft + "px";
		elemnt.style.top = elemnt.offsetTop + "px";

		for (var ceil_id = 0; ceil_id < ceils.length; ceil_id++) {
			var ceil = ceils[ceil_id];
			if (ceil === div_parent) {
				moveFrom = ceil_id;
			}
		}

		document.onmouseup = closeDragElement;
		document.onmousemove = elementDrag;


	}

	function elementDrag(el) {

		el = el || window.event;

		pos1 = elemnt.offsetLeft + (curX - curXprev);
		pos2 = elemnt.offsetTop + (curY - curYprev);

		elemnt.style.left = pos1 + "px";
		elemnt.style.top = pos2 + "px";

		var visited = false
		for (var ceil_id = 0; ceil_id < ceils.length; ceil_id++) {
			var ceil = ceils[ceil_id];
			if (ceil !== div_parent) {

				var ax = ceil.offsetLeft, ay = ceil.offsetTop, aw = ceil.offsetWidth, ah = ceil.offsetHeight;
				
				if (curX >= ax && curX <= ax+aw && curY >= ay && curY <= ay+ah) {
					ceil.style["background-color"] = "#C8EEC8";
					moveTo = ceil_id;
					visited = true;
				} else {
					ceil.style.removeProperty("background-color");
				}
			}
		}

		if (visited) {

			elemnt.style["background-color"] = "#9EEE9E";
		} else {

			elemnt.style["background-color"] = "#FFD9CC";
		}

		curXprev = curX;
		curYprev = curY;

	}

	function closeDragElement() {

		document.onmouseup = null;
		document.onmousemove = null;
		elemnt.style.position = "relative";

		elemnt.style.removeProperty("border");

		elemnt.style.removeProperty("left");
		elemnt.style.removeProperty("top");

		elemnt.style.removeProperty("width");
		elemnt.style.removeProperty("height");

		isMouseDown = false;

		elemnt.style["background-color"] = "#EEEEEE";

		if (div_dragger !== null) {
			div_dragger.style.border = "1px solid black";
		}
		if (div_element !== null) {
			div_element.style.removeProperty("display");
		}
		if (div_redblock !== null) {

			div_redblock.style.display = "none";
		}

		for (ceil of ceils) {

			ceil.style.removeProperty("background-color");
		}
 
		var result = elemnt.getAttribute("name") + ", " + moveFrom + ", " + moveTo;
		flaskEditor.value = result;

		//location.reload();
		document.getElementById("Accept").click();

	}

}