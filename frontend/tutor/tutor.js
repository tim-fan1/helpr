///////////////////////////////////////////////////////////
// global variables.
///////////////////////////////////////////////////////////

const backendURL = "http://127.0.0.1:8080";

///////////////////////////////////////////////////////////
// bootstrap.
///////////////////////////////////////////////////////////

// get current login.
const isTutor = window.sessionStorage.getItem("isTutor");
const zid = window.sessionStorage.getItem("zid");

// if current login is invalid.
if (!(zid && isTutor)) {
	// redirect user to the login page.
	window.location.href = "/";
}

// otherwise, perform callback function on page load.
window.onload = function () {

	// fill in greeting.
	document.getElementById("greeting").appendChild(function () {
		const p = document.createElement("p");
		p.appendChild(document.createTextNode(`hello tutor ${zid}.`));
		return p;
	}());

	// fill in requestList.
	loadQueue();

	// disable end session button if current tutor is not admin.
	const endSessionButton = document.getElementById("endSessionButton");
	endSessionButton.disabled = (zid !== "admin");

	// add event listener for end session button click.
	endSessionButton.addEventListener("click", event => {
		event.preventDefault();
		// send request to backend.
		let xmlhttp = new XMLHttpRequest();
		xmlhttp.open("DELETE", `${backendURL}/end`, true);
		xmlhttp.onreadystatechange = function () {
			// when request has finished refill requestList.
			if (this.readyState === 4 && this.status === 200) {
				loadQueue();
			}
		};
		xmlhttp.send();
	});

}

///////////////////////////////////////////////////////////
// helper functions.
///////////////////////////////////////////////////////////

/**
 * Refills the requestList element.
 */
function loadQueue() {
	// send queue request.
	let xmlhttp = new XMLHttpRequest();
	xmlhttp.open("GET", `${backendURL}/queue`, true);
	// process queue request.
	xmlhttp.onreadystatechange = function () {
		if (this.readyState === 4 && this.status === 200) {
			// the returned queue of requests from backend.
			let queue = JSON.parse(this.responseText);
			processQueueRequest(queue);
		}
	}
	xmlhttp.send();
}

/**
 * Fills in the request list element given a queue.
 * @param {object} queue a list of requests.
 */
function processQueueRequest(queue) {
	if (queue.length === 0) {
		document.getElementById("requestList").innerHTML = "no requests in queue.";
	} else {
		// first empty the list.
		document.getElementById("requestList").innerHTML = "";
		// now add items from returned queue to the empty list.
		for (let i = 0; i < queue.length; i++) {
			let li = document.createElement("li");
			li.appendChild(document.createTextNode(`zid: ${queue[i]["zid"]}. `));
			li.appendChild(document.createTextNode(`description: ${queue[i]["description"]}. `));
			li.appendChild(document.createTextNode(`status: ${queue[i]["status"]}.`));
			// append form element containing four button elements.
			li.appendChild(function (request) {
				let form = document.createElement("form");
				// each button has an event listener attached.
				form.appendChild(generateButton(request, "help"));
				form.appendChild(generateButton(request, "resolve"));
				form.appendChild(generateButton(request, "revert"));
				return form;
			}(queue[i]));
			// add item to list.
			document.getElementById("requestList").appendChild(li);
		}
	}
}

/**
 * generate button element (with click event listener attatched).
 * @param {object} request contains a status, zid, and description key.
 * @param {string} type (resolve|revert|help|cancel).
 */
function generateButton(request, type) {
	let button = document.createElement("button");
	button.appendChild(document.createTextNode(`${type}`));
	// disallow cases where backend will throw BAD_REQUEST.
	if (request["status"] === "waiting" && (type === "resolve" || type === "revert")) {
		button.disabled = true;
	} else if (request["status"] === "receiving" && (type === "help" || type === "cancel")) {
		button.disabled = true;
	}
	// attach event listener to button.
	button.addEventListener("click", event => {
		event.preventDefault();
		const zid = request["zid"];
		const requestBody = JSON.stringify({
			"zid": zid,
		});
		// send request to backend.
		let xmlhttp = new XMLHttpRequest();
		const method = (type === "help" || type === "revert") ? "POST" : "DELETE";
		xmlhttp.open(method, `${backendURL}/${type}`, true);
		xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		xmlhttp.onreadystatechange = function () {
			// when request has finished reload queue.
			if (this.readyState === 4 && this.status === 200) {
				loadQueue();
			}
		};
		xmlhttp.send(requestBody);
	})
	return button;
}
