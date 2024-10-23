function verify_credentials() {
  // Get username and password values
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  // Check if either username or password is empty
  if (!username || !password) {
    // Redirect to bmu.html if any field is empty
    window.location.href = "bmu.html";
    return false; // Prevent further execution
  }

  // AJAX call for verifying credentials
  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/login", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4) {
      if (this.status == 200) {
        window.location.href = "/dashboard"; // Successful login
      } else {
        document.getElementById("error").innerHTML =
          "Either username or password is incorrect!";
      }
    }
  };
  
  // Send the request with encoded username and password
  xhttp.send(
    "username=" + encodeURIComponent(username) +
    "&password=" + encodeURIComponent(password)
  );

  return false; // Prevent form submission
}
