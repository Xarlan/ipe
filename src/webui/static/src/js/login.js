let login_btn = document.getElementById("login");

login_btn.addEventListener("click", (event)=>{
    event.preventDefault();
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    fetch(SERVER_PROTO + SERVER_HOST + "/authenticate", {
        method: "post",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                email: email,
                password: password
            }
        )
    })
    .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.status === 1){
                window.location = SERVER_PROTO + SERVER_HOST;
            } else if(data.status === 2) {
                alert("No such user or incorrect password");
            }

        })
        .catch(error => alert("Some error during authorization occured"))
});
