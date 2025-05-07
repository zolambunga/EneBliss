
 //Função para alternar entre mostrar e esconder senha


  document.addEventListener('DOMContentLoaded', function()
  {
    const password1Field = document.getElementById('password1');
    const password2Field = document.getElementById('password2');
    const togglePassword1 = document.getElementById('togglePassword1');
    const togglePassword2 = document.getElementById('togglePassword2');

    function togglePassword(passwordField, passwordIcon)
    {
      const passwordType = passwordField.type;

      // Alterne entre 'password' (ocultar) e 'text' (mostrar)
      if (passwordType === "password")
      {
        passwordField.type = "text"; //Torna a senha visível
        passwordIcon.classList.remove('fa-eye-slash');// remove o icon de olho fechado
        passwordIcon.classList.add('fa-eye');// Adiciona o icon de olho fechado
      }
      else
       {
         passwordField.type = "password"; // Torna invisivel a senha
         passwordIcon.classList.remove('fa-eye'); //Remove o icone do olho fechado
         passwordIcon.classList.add('fa-eye-slash'); //Adiciona o icone de olho aberto
       }
    }
    // Adicionar evento de clique nos icones
    togglePassword1.addEventListener('click', function()
      {
        togglePassword(password1Field, togglePassword1);
      }
    )

    togglePassword2.addEventListener('click', function()
      {
        togglePassword(password2Field, togglePassword2);
      }
    )
  }
)