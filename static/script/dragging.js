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
	var moveFrom = -1, moveTo = -1;
	var elemntInner = elemnt.innerHTML;

	elemnt.onmousedown = dragMouseDown;
	elemnt.onmouseover = mouseOver;
	elemnt.onmouseout = mouseOut;

	var divElements = document.getElementsByClassName("divElements");
	var divElement = null;
	var divRedBlock = null;

	var divParent = null;


	var divColumns = document.getElementsByClassName("divTableHead");
	var divColumnNames = []
	for (var elem of divColumns) {
		divColumnNames.push(elem.innerHTML);
	}

	var divRows = document.getElementsByClassName("divTableSideCell");
	var divRowNames = []
	for (var elem of divRows) {
		var divTag = elem.getElementsByTagName("p")[0]
		divRowNames.push(divTag.innerHTML);
	}


	for (var elem of divElements) {
		if (elem.getAttribute("name") === elemnt.getAttribute("name")) {

			if (elem.getAttribute("id") === "divRedBlock") {

				divRedBlock = elem;

			} else {

				divElement = elem;
			}
		}
	}

	var divDragBlocks = document.getElementsByClassName("divDrag");
	var divDragger = null;

	var cells = document.getElementsByClassName("divTableCell")

	for (var elem of divDragBlocks) {
		if (elem.getAttribute("name") === elemnt.getAttribute("name")) {
			divDragger = elem;
			divParent = elem.parentNode.parentNode
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

		if (divDragger !== null) {
			divDragger.style.border = "0px solid black";
		}

		if (divElement !== null) {

			divElement.style.display = "none";
		}
		if (divRedBlock !== null) {

			divRedBlock.style.display = "block";
			divRedBlock.style.width = width+"px";
			divRedBlock.style.height = width+"px";
		}

		elemnt.style.width = width+"px";
		elemnt.style.height = height+"px";

		elemnt.style.left = elemnt.offsetLeft + "px";
		elemnt.style.top = elemnt.offsetTop + "px";

		for (var cellId = 0; cellId < cells.length; cellId++) {
			var cell = cells[cellId];
			if (cell === divParent) {
				moveFrom = cellId;
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
		for (var cellId = 0; cellId < cells.length; cellId++) {
			var cell = cells[cellId];
		
			if (cell !== divParent && !visited) {

				var ax = cell.offsetLeft, ay = cell.offsetTop, aw = cell.offsetWidth, ah = cell.offsetHeight;
				
				if (curX >= ax && curX <= ax+aw && curY >= ay && curY <= ay+ah) {
					cell.style["background-color"] = "#C8EEC8";

					var rowId = Math.floor(cellId/divColumns.length);
					var colId = cellId - rowId*divColumns.length;

					elemnt.innerHTML = divRowNames[rowId] + divColumnNames[colId]; 

					moveTo = cellId;
					visited = true;
				} else {
					cell.style.removeProperty("background-color");
					elemnt.innerHTML = "<i>Пусто</i>";
					moveTo = -1;
				}
			} else {
				cell.style.removeProperty("background-color");
				if (!visited) {
					moveTo = -1;
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
		elemnt.innerHTML = elemntInner;


		elemnt.style.removeProperty("border");

		elemnt.style.removeProperty("left");
		elemnt.style.removeProperty("top");

		elemnt.style.removeProperty("width");
		elemnt.style.removeProperty("height");

		isMouseDown = false;

		elemnt.style["background-color"] = "#EEEEEE";

		if (divDragger !== null) {
			divDragger.style.border = "1px solid black";
		}
		if (divElement !== null) {
			divElement.style.removeProperty("display");
		}
		if (divRedBlock !== null) {

			divRedBlock.style.display = "none";
		}

		for (var cell of cells) {

			cell.style.removeProperty("background-color");
		}
 
 		if (moveTo >= 0) {

			var result = elemnt.getAttribute("name") + ", " + moveFrom + ", " + moveTo;
			flaskEditor.value = result;

			//location.reload();
			document.getElementById("Accept").click();
 		}

	}

}