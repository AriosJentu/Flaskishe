function load_base() {
	var combobox = document.getElementById("List");
	var seltext = combobox.options[combobox.selectedIndex].text;
	var port = document.location.port;
	var locate = "http://"+document.location.hostname;
	if (port > 1000) {
		locate += ":"+port;
	}
	locate += "/table/"+seltext;
	document.location.href = locate;
	alert(locate);
}