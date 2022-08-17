function validateForm() {
  let username = document.getElementById('email').value;
  let password = document.getElementById('password').value;

  if (username === "") {
      alert('please Enter an Email !');
      return false;


// Validate with regex later

  } else {
      if (password === "") {
        alert('please Enter a Password !');
        return false;
      }     
  }
}