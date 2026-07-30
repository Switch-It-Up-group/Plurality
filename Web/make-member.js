const form = document.getElementById("member-form");
const params = new URLSearchParams(window.location.search);

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);

    const member = {
        name: formData.get("name"),
        pronouns: formData.get("pronouns"),
        color: formData.get("color")
    };

    localStorage.setItem("newMember", JSON.stringify(member));


    const oldmembers = JSON.parse(localStorage.getItem("members"));
    oldmembers[crypto.randomUUID()] = {
        name: formData.get("name"),
        pronouns: formData.get("pronouns"),
        description: formData.get("description"),
        metadata: {
            color: formData.get("color")
        },
        archived: false
    };
    localStorage.setItem("members", JSON.stringify(oldmembers));

    if (window.opener) {
        window.close();
    } else {
        window.location.href = "index.html";
    }

});