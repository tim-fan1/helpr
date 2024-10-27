///////////////////////////////////////////////////////////
// global variables.
///////////////////////////////////////////////////////////

const backendURL = "http://127.0.0.1:8080";

///////////////////////////////////////////////////////////
// bootstrap.
///////////////////////////////////////////////////////////

// get current login.
const isStudent = window.sessionStorage.getItem("isStudent");
const zid = window.sessionStorage.getItem("zid");

// if current login is invalid.
if (!(zid && isStudent)) {
	// redirect user to the login page.
	window.location.href = "/";
}

// otherwise, perform callback function on page load.
window.onload = function() {

	// fill in greeting.
	document.getElementById("greeting").appendChild(function () {
		const p = document.createElement("p");
		p.appendChild(document.createTextNode(`hello student ${zid}.`));
		return p;
	}());

	// add event listener for make request form submission.
	document.getElementById("makeRequestForm").addEventListener("submit", event => {
		event.preventDefault();
		// create json request body from makeRequestForm information.
		const description = makeRequestForm["description"].value;
		const requestBody = JSON.stringify({
			// taken from sessionStorage.
			"zid": zid,
			"description": description,
		});
		console.log("here");
		// send request to backend.
		let xmlhttp = new XMLHttpRequest();
		xmlhttp.open("POST", `${backendURL}/make_request`, true);
		xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		xmlhttp.onreadystatechange = function () {
			// when request has finished reset request status.
			if (this.readyState === 4 && this.status === 200) {
				loadRequestStatus();
			}
		};
		xmlhttp.send(requestBody);
	});

	// set this student's request status.
	loadRequestStatus();
	
}

/**
 * Sends and processes queue request to fill in this student's request status.
 */
function loadRequestStatus() {
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
 * Fills in request status element given a queue.
 * @param {object} queue a list of requests.
 */
function processQueueRequest(queue) {
	// reset old request status.
	const requestStatus = document.getElementById("requestStatus");
	requestStatus.innerHTML = "";
	requestStatus.appendChild(document.createTextNode("please make a request"));
	// load new request status.
	for (let i = 0; i < queue.length; i++) {
		if (queue[i]["zid"] === zid) {
			requestStatus.innerHTML = "";
			if (queue[i]["status"] === "waiting") {
				requestStatus.appendChild(document.createTextNode("your request is waiting for a tutor to help."));
			} else {
				requestStatus.appendChild(document.createTextNode("your request is being received by a tutor."));
			}
			requestStatus.appendChild(generateCancelButton(queue[i]));
			break;
		}
	}
	// if control reaches here, zid not found, status will be default status.
	return;
}

/**
 * generate cancel button element for this student's request.
 * @param {object} request contains status key.
 */
function generateCancelButton(request) {
	let button = document.createElement("button");
	button.appendChild(document.createTextNode("cancel"));
	// disable button if it is being received.
	button.disabled = (request["status"] === "receiving");
	// attach event listener to button.
	button.addEventListener("click", event => {
		event.preventDefault();
		const requestBody = JSON.stringify({
			"zid": zid,
		});
		// send request to backend.
		let xmlhttp = new XMLHttpRequest();
		xmlhttp.open("DELETE", `${backendURL}/cancel`, true);
		xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		xmlhttp.onreadystatechange = function () {
			// when request has finished reset request status.
			if (this.readyState === 4 && this.status === 200) {
				loadRequestStatus();
			}
		};
		xmlhttp.send(requestBody);
	})
	return button;
}