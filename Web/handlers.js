const open_btn = document.getElementById("open");
const membersdiv = document.getElementById("members");
const create_member_btn = document.getElementById("create_member");
const export_btn = document.getElementById("export");

function build(jsonfile) {
    membersdiv.replaceChildren();
    for (const uid in jsonfile) {
        const memberdiv = document.createElement("div")
        
        const memdat = jsonfile[uid];
        const memname = document.createElement("h3");
        const mempro = document.createElement("h5");
        const memdesc = document.createElement("p");

        memberdiv.id = uid + "-div";

        memname.textContent = memdat["name"];
        mempro.textContent = memdat["pronouns"]
        memdesc.textContent = memdat["description"]

        if ("metadata" in memdat) {
            if ("color" in memdat["metadata"]) {
                memberdiv.style = 'background: linear-gradient(to bottom, #202020, ' + memdat["metadata"]["color"] + '70);'
            };
        };


        memberdiv.className = "member";

        memberdiv.appendChild(memname);
        if (memdat["pronouns"] != "") {
            memberdiv.appendChild(mempro);
        }
        
        if (memdat["description"] != "") {
            memberdiv.appendChild(memdesc);
        }


        membersdiv.appendChild(memberdiv);

    }

};

function downloadJSON(data, filename = "members.json") {
    const jsonText = JSON.stringify(data, null, 4);

    const blob = new Blob([jsonText], {
        type: "application/json"
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = filename;

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
}

build(JSON.parse(localStorage.getItem("members") ?? "{}"))

open_btn.addEventListener("change", async function () {
    const file = open_btn.files[0];
    const jdata = await file.text();
    const jsondat = JSON.parse(jdata);
    console.log(file.text());
    build(jsondat);
    localStorage.setItem("members", jdata)
});


create_member_btn.addEventListener("click", function () {
    const isMobile = window.matchMedia("(max-width: 600px)").matches;

    if (isMobile) {
        window.location.href = "createmember.html";
        return;
    }

    const createMemberWindow = window.open(
        "createmember.html",
        "createMember",
        "width=500,height=600"
    );

    if (!createMemberWindow) {
        window.location.href = "createmember.html";
        return;
    }

    const closeCheck = setInterval(function () {
        if (createMemberWindow.closed) {
            clearInterval(closeCheck);

            build(
                JSON.parse(localStorage.getItem("members") ?? "{}")
            );
        }
    }, 250);
});

export_btn.addEventListener("click", function () {
    downloadJSON(JSON.parse(localStorage.getItem("members") ?? "{}"), "members.json");
});