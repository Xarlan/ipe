///////////////////////////////////  Scope page     ///////////////////////////////
let scope_import_btn = document.getElementsByClassName("scope__add-btn")[0];
let toggle_all_btn = document.getElementById("get-all");
let delete_selected_btn = document.getElementsByClassName("scope__delete")[0];

scope_import_btn.addEventListener("click", event => {
    event.preventDefault();
    let scope_hosts = document.querySelector("input[name=scope_hosts]");
    let reader = new FileReader();

    if(scope_hosts.files.length) {
        reader.readAsText(scope_hosts.files[0]);

        reader.onload = function() {
            fetch(SERVER_PROTO + SERVER_HOST + "/api/project/importScope", {
                method: "post",
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        project_id: project_id,
                        scope_hosts: reader.result
                    }
                )
            })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    if(data.status === 1) {
                        let scope_modal_elem = document.getElementById('scopeModal');
                        let scope_modal = coreui.Modal.getInstance(scope_modal_elem);
                        scope_modal.hide();
                        let success_modal = new coreui.Modal(document.getElementById('successModal'));
                        success_modal.show();
                        document.getElementById('successModal').addEventListener('hide.coreui.modal', (e)=>{
                            window.location = "";
                        },false);
                    } else {
                        alert(data.error)
                    }
                })
                .catch(error => alert(error))
        };
    }
});

toggle_all_btn.addEventListener("click", (e)=>{
    let checkboxes = document.getElementsByClassName("host-chbox");
    if (!e.target.checked) {
        for (let i=0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
    } else {
        for (let i=0; i < checkboxes.length; i++) {
            checkboxes[i].checked = true;
        }
    }
});

delete_selected_btn.addEventListener("click", ()=>{
    let hosts_for_delete = [];
    let chboxes = document.getElementsByClassName("host-chbox");
    [].forEach.call(chboxes, (chbox)=>{
        if(chbox.checked) {
           let tr = chbox.closest("tr");
           let ip = tr.querySelector(".scope__ip");
           let domain = tr.querySelector(".scope__domain");
           if (ip.innerHTML !== "-") {
               hosts_for_delete.push(ip.innerHTML);
           }
           if (domain.innerHTML !== "-") {
               hosts_for_delete.push(domain.innerHTML);
           }
        }
    });
    if (hosts_for_delete.length) {
        fetch(SERVER_PROTO + SERVER_HOST + "/api/project/deleteScope", {
            method: "post",
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                project_id : project_id,
                delete_hosts: hosts_for_delete
            })
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.status === 1) {
                let delete_modal = new coreui.Modal(document.getElementById('deleteModal'));
                delete_modal.show();
                document.getElementById('deleteModal').addEventListener('hide.coreui.modal', (e)=>{
                    window.location = "";
                },false);
            } else if (data.status === 0) {
                alert(data.error);
            }
        })
        .catch(error => {
            alert(error);
        });
    }
});