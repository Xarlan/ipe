///////////////////////////////////  Projects page     ///////////////////////////////
let project_add_btn = document.getElementsByClassName("project__add-btn")[0];
project_add_btn.addEventListener("click", event=>{
    event.preventDefault();
    let name = document.querySelector("input[name=name]").value;
    let description = document.querySelector("input[name=description]").value;
    let date_from = document.querySelector("input[name=date_from]").value;
    let date_to = document.querySelector("input[name=date_to]").value;
    let host_history = document.querySelector("input[name=host_history]").value;
    let retro_delete = document.getElementsByName("retro_delete"),
        checked_retro;

    for (let i=0; i < retro_delete.length; i++) {
        if (retro_delete[i].checked) {
            checked_retro = retro_delete[i].value;
        }
    }

    let data = {
        name: name,
        description: description,
        date_from: Date.parse(date_from)/1000,
        date_to: Date.parse(date_to)/1000,
        host_history: host_history,
        retro_delete: checked_retro
    };

    fetch(SERVER_PROTO + SERVER_HOST + "/api/createProject", {
        method: "post",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.status === 1) {
                window.location = "/";
            } else if (data.satus === 0) {
                alert(data.data);
            }
        })
        .catch(error => alert(error))
});