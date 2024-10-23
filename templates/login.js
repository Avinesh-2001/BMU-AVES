function verify_credentials() {
  // TODO: Implement correct AJAX call here
  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/login", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.onreadystatechange = function () {
    if (this.status == 200) {
      window.location.href = "/dashboard";
    } else {
      document.getElementById("error").innerHTML =
        "Either username or password is incorrect!";
    }
  };
  xhttp.send(
    "username=" +
      encodeURIComponent(document.getElementById("username").value) +
      "&password=" +
      encodeURIComponent(document.getElementById("password").value)
  );
  return false;
}
