let vuln_delete_btn = document.getElementsByClassName("vuln__delete-btn")[0];
let vuln_edit_btn = document.getElementsByClassName("vuln__edit-btn")[0];
let attach_upload_btn = document.getElementsByClassName("attach__upload")[0];

vuln_delete_btn.addEventListener("click", () => {
    let is_delete = confirm("Are you sure you want to delete vuln ?");
    if (is_delete) {
        fetch(SERVER_PROTO + SERVER_HOST + "/api/deleteVulnerability", {
            method: "post",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                {
                    vuln_id: vuln_id
                }
            )
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data.status === 1) {
                    window.location = SERVER_PROTO + SERVER_HOST + "/project/" + project_id;
                } else {
                    alert(data.error)
                }
            })
            .catch(error => alert(error))
    }
});

vuln_edit_btn.addEventListener("click", () => {
    let name = document.querySelector("input[name=name]").value;
    let full_path = document.querySelector("input[name=full_path]").value;
    let description = document.querySelector("textarea[name=description]").value;
    let risk = document.querySelector("textarea[name=risk]").value;
    let details = document.querySelector("textarea[name=details]").value;
    let recommendation = document.querySelector("textarea[name=recommendation]").value;
    let context_elems = document.getElementsByClassName("vuln__context"),
        checked_context;
    let criticality_inputs = document.querySelectorAll("input[name=criticality]"),
        checked_criticality;
    let probability_inputs = document.querySelectorAll("input[name=probability]"),
        checked_probability;
    let target = document.getElementById("vuln-target").value,
        hosts;
    if (target.length) {
        hosts = target.split(",").filter(host => {
            return host.trim().length > 0
        }).map(host => {
            return host.trim()
        });
    }

    for (let i = 0; i < context_elems.length; i++) {
        if (context_elems[i].checked) {
            checked_context = context_elems[i].value;
        }
    }

    for (let i = 0; i < criticality_inputs.length; i++) {
        if (criticality_inputs[i].checked) {
            checked_criticality = criticality_inputs[i].value;
        }
    }

    for (let i = 0; i < probability_inputs.length; i++) {
        if (probability_inputs[i].checked) {
            checked_probability = probability_inputs[i].value;
        }
    }

    fetch(SERVER_PROTO + SERVER_HOST + "/api/editVulnerability", {
        method: "post",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                project_id: project_id,
                vuln_id: vuln_id,
                name: name,
                object: checked_context,
                full_path: full_path,
                criticality: checked_criticality,
                probability: checked_probability,
                final_criticality: Math.floor((Number(checked_criticality) + Number(checked_probability)) / 2),
                description: description,
                risk: risk,
                details: details,
                recommendation: recommendation,
                target: hosts && hosts.length && hosts.length > 0 ? hosts : []
            }
        )
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.status === 1) {
                window.location = "";
            } else {
                alert(data.error)
            }
        })
        .catch(error => alert(error))
});



let attach_number = 1;
let create_item_flag = [];

window.handle_attach = function (target){
    let attach_item = target.closest("li");
    attach_item.querySelector(".attach__name").innerText = target.files[0].name;
    if (!create_item_flag.includes(target.id)){
        create_item_flag.push(target.id);
        let attach_list = document.getElementsByClassName("attach__list")[0];
        let attach_clone = document.createElement('li');
        attach_number++;
        attach_clone.className = "attach__item";
        attach_clone.innerHTML = `<label for="uploadbtn-${attach_number}" class="btn btn-outline-primary scope__add-btn uploadButton">choose attach</label>
                          <input class="attach__input" type="file" id="uploadbtn-${attach_number}" accept=".jpg,.jpeg,.png" onchange="handle_attach(this)">
                          <input type="text" id="attach__description" class="attach__description form-control" name="attach__description" placeholder="description">
                          <span class="attach__name"></span>
                          <span class="attach__item-close disabled" onclick="this.closest('li').parentNode.removeChild(this.closest('li'));">X</span>`;
        attach_list.appendChild(attach_clone);
    }

    if(attach_item.querySelector(".attach__item-close.disabled")){
        attach_item.querySelector(".attach__item-close.disabled").classList.remove("disabled");
    }
};

attach_upload_btn.addEventListener("click", ()=>{
   let attaches = document.getElementsByClassName("attach__input");

   for (let i=0; i < attaches.length; i++){
       if(attaches[i].files[0]){
           let attach_dom_el = attaches[i];
           let attach_description = attaches[i].closest(".attach__item").querySelector(".attach__description").value;
           let formData = new FormData();
           formData.append("attach", attaches[i].files[0]);
           formData.append("vuln_id", vuln_id);
           formData.append("description", attach_description);

           let uploaded_attach_block = document.getElementsByClassName("attach__existed")[0];

           fetch(SERVER_PROTO + SERVER_HOST + '/api/uploadFile', {
               method: "post",
               body: formData
           })
               .then(response => {
                    return response.json();
                })
                .then(data => {
                    if (data.status === 1) {
                        let new_attach = document.createElement('li');
                        new_attach.innerHTML = `<a href="/api/getAttach/${data.id}" target="_blank">${data.filename}</a> - <span>${attach_description.replace(/&/g, "&amp;").replace(/>/g, "&gt;").replace(/</g, "&lt;").replace(/"/g, "&quot;")}</span> - <button class="btn btn-outline-danger attach__delete" onclick="delete_attach(event, ${data.id})">delete</button>`;
                        uploaded_attach_block.appendChild(new_attach);
                        attach_dom_el.closest("li").parentNode.removeChild(attach_dom_el.closest('li'));
                    } else {
                        alert(data.error)
                    }
                })
                .catch(error => alert(error))
       }
   }
});

window.delete_attach = function(event, id){
    event.preventDefault();
    let is_delete = confirm("Are you sure you want to delete attachment ?");
    if (is_delete){
            fetch(SERVER_PROTO + SERVER_HOST + "/api/deleteAttach/", {
            method: "post",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: id
            })
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data.status === 1) {
                    atta_item = event.target.closest("li");
                    atta_item.parentNode.removeChild(atta_item);
                } else {
                    alert(data.error)
                }
            })
            .catch(error => alert(error))
    }
};