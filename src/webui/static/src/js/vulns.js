let vuln_add_btn = document.getElementsByClassName("vuln__add-btn")[0];

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