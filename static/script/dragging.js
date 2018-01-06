//dragElement(document.getElementById("divdrg"))

var elements = document.getElementsByClassName("divDragger")

for (var element of elements) {
	dragElement(element);
}

var curX = null, curY = null;
document.addEventListener('mousemove', onMouseUpdate, false);
document.addEventListener('mouseenter', onMouseUpdate, false);
var spt = document.getElementById("titledebug");
function onMouseUpdate(e) {
    curX = e.pageX;
    curY = e.pageY;
}

function dragElement(elemnt) {

	var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
	var width = null, height = null;
	var is_mouse_down = false

	elemnt.onmousedown = dragMouseDown;
	elemnt.onmouseover = mouseOver;
	elemnt.onmouseout = mouseOut;

	var div_elements = document.getElementsByClassName("divElements");
	var div_element = null;
	var div_redblock = null;


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

	for (var div_drg of div_drag_blocks) {
		if (div_drg.getAttribute("name") === elemnt.getAttribute("name")) {
			div_dragger = div_drg;
		}
	}

	function mouseOver(el) {
		if (!is_mouse_down) {

			elemnt.style["background-color"] = "#9EEE9E";
		}
	}

	function mouseOut(el) {
		if (!is_mouse_down) {

			elemnt.style["background-color"] = "#EEEEEE";
		}
	}


	function dragMouseDown(el) {
	
		
		el = el || window.event;

		pos3 = el.clientX;
		pos4 = el.clientY;
		width = elemnt.offsetWidth;
		height = element.offsetHeight;
		is_mouse_down = true;

		
		elemnt.style.position = "absolute";
		elemnt.style.border = "1px solid black";
		elemnt.style["background-color"] = "#ffD9CC";

		if (div_dragger !== null) {
			div_dragger.style.border = "0px solid black";
			spt.innerHTML = "Found"
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

		//spt.innerHTML = "Start Positions:\nX: " + pos3 + "; Y:" + pos4 + ";\nFROM:\nX: " + elemnt.offsetLeft + "; Y: " + elemnt.offsetTop + ";";

		document.onmouseup = closeDragElement;
		document.onmousemove = elementDrag;


	}

	function elementDrag(el) {

		//alert("Dragging "+elemnt.getAttribute("name"));
		el = el || window.event;

		pos1 = pos3 - el.clientX;
		pos2 = pos4 - el.clientY;
		pos3 = el.clientX;
		pos4 = el.clientY;

		elemnt.style.left = (elemnt.offsetLeft - pos1) + "px";
		elemnt.style.top = (elemnt.offsetTop - pos2) + "px";

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

		is_mouse_down = false;

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
	}

}