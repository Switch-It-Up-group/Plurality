const open_btn = document.getElementById("open");
const membersdiv = document.getElementById("members");

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



open_btn.addEventListener("change", async function () {
    const file = open_btn.files[0];
    const jdata = await file.text();
    const jsondat = JSON.parse(jdata);
    console.log(file.text());
    build(jsondat);
});