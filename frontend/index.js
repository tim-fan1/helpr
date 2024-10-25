///////////////////////////////////////////////////////////
// bootstrap.
///////////////////////////////////////////////////////////

// perform callback function on page load.
window.onload = function() {
	document.getElementById("studentForm").addEventListener("submit", (event) => {
		event.preventDefault();
		// get the student's zid from the form.
		const studentForm = document.getElementById("studentForm");
		const zid = studentForm["zid"].value;
		// record the student's zid into sessionStorage.
		// this will then be used to identify who is the current active student.
		window.sessionStorage.clear();
		window.sessionStorage.setItem("isStudent", true);
		window.sessionStorage.setItem("zid", zid);
		console.log(`student ${sessionStorage.getItem("zid")} is now logged in.`);
		// redirect to student page.
		window.location.href += "student";
	});

	document.getElementById("tutorForm").addEventListener("submit", (event) => {
		event.preventDefault();
		// get the tutor's zid from the form.
		const tutorForm = document.getElementById("tutorForm");
		const zid = tutorForm["zid"].value;
		// record the tutor's zid into sessionStorage.
		// this will then be used to identify who is the current active tutor.
		window.sessionStorage.clear();
		window.sessionStorage.setItem("isTutor", true);
		window.sessionStorage.setItem("zid", zid);
		console.log(`tutor ${sessionStorage.getItem("zid")} is now logged in.`);
		// redirect to tutor page.
		window.location.href += "tutor";
	});
}