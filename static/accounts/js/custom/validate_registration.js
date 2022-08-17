function validateForm() {
  let form_fields = document.getElementsByTagName('input')

  let username = form_fields[1].value;
  let email = form_fields[2].value;
  let password1 = form_fields[3].value;
  let password2 = form_fields[4].value;

  if (username === "") {
      alert('please Enter a Username !');
      return false;

  } else {
      if (email === "") {
        alert('please Enter an Email !');
        return false;
      }   
      else {
        if (password1 === "") {
          alert('please Enter a Password !');
          return false;
        }  
        else {
          if (password2 === "") {
            alert('please Confirm your Password !');
            return false;
          }     

          else {
            if (password1 != password2 ) {
              alert('Passwords do not Match !');
              return false;
            }     
        }
      }   
    }
  }

}