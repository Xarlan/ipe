let vuln_add_btn = document.getElementsByClassName("vuln__add-btn")[0];
let create_report_vuln_btn = document.getElementById("report-per-vuln");
let create_report_host_btn = document.getElementById("report-per-host");

vuln_add_btn.addEventListener("click", (event)=>{
    event.preventDefault();

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
        hosts = target.split(",").filter(host=>{return host.trim().length > 0}).map(host=>{return host.trim()});
    }

    for (let i=0; i < context_elems.length; i++) {
        if (context_elems[i].checked) {
            checked_context = context_elems[i].value;
        }
    }

    for (let i=0; i < criticality_inputs.length; i++) {
        if (criticality_inputs[i].checked) {
            checked_criticality = criticality_inputs[i].value;
        }
    }

    for (let i=0; i < probability_inputs.length; i++) {
        if (probability_inputs[i].checked) {
            checked_probability = probability_inputs[i].value;
        }
    }

    fetch(SERVER_PROTO + SERVER_HOST + "/api/createVulnerability", {
        method: "post",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                project_id: project_id,
                name: name,
                object: checked_context,
                full_path: full_path,
                criticality: checked_criticality,
                probability: checked_probability,
                final_criticality: Math.floor((Number(checked_criticality) + Number(checked_probability))/2),
                description: description,
                risk: risk,
                details: details,
                recommendation: recommendation,
                target: hosts && hosts.length && hosts.length > 0  ? hosts : []
            }
        )
    })
    .then(response => {
        return response.json();
    })
        .then(data=>{
            if(data.status === 1) {
                window.location = "";
            } else {
                alert(data.error)
            }
        })
    .catch(error => alert(error))
});


create_report_vuln_btn.addEventListener("click", (event)=>{
    event.preventDefault();
    let form = document.createElement("form");
    form.className = "report__form";
    form.setAttribute("action", SERVER_PROTO + SERVER_HOST + "/report/vuln/" + project_id);
    form.setAttribute("target", "_blank");
    document.body.append(form);
    form.submit()
});

create_report_host_btn.addEventListener("click", event=> {
    event.preventDefault();
    let form = document.createElement("form");
    form.className = "report__form";
    form.setAttribute("action", SERVER_PROTO + SERVER_HOST + "/report/host/" + project_id);
    form.setAttribute("target", "_blank");
    document.body.append(form);
    form.submit()
});