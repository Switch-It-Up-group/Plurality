const open_btn = document.getElementById("open");
const membersdiv = document.getElementById("members");

function build(jsonfile) {
    membersdiv.replaceChildren();
    for (const uid in jsonfile) {
        const memberdiv = document.createElement("div")
        
        const memdat = jsonfile[uid];
        const memname = document.createElement("h3");
        const mempro = document.createElement("h5");

        memberdiv.id = uid + "-div";

        memname.textContent = memdat["name"];
        mempro.textContent = memdat["pronouns"]


        memberdiv.className = "member";

        memberdiv.appendChild(memname);
        memberdiv.appendChild(mempro);


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