import {
    auth,
    database,
    ref,
    set,
    push,
    onAuthStateChanged
} from "./server-auth.js";

const form = document.getElementById("member-form");
const returnBtn = document.getElementById("return");
const memberMessage = document.getElementById("member-message");

let currentUser = null;
let authFinishedLoading = false;

function returnToMembers() {
    if (window.opener && !window.opener.closed) {
        window.close();
        return;
    }

    window.location.href = "index.html";
}

returnBtn.addEventListener("click", function () {
    returnToMembers();
});

onAuthStateChanged(auth, function (user) {
    authFinishedLoading = true;
    currentUser = user;

    if (!user) {
        memberMessage.textContent =
            "You must sign in before creating a member.";

        form.hidden = true;

        window.setTimeout(function () {
            window.location.href = "index.html";
        }, 1500);

        return;
    }

    memberMessage.textContent =
        `Signed in as ${user.email ?? user.uid}`;
});

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (!authFinishedLoading) {
        memberMessage.textContent =
            "Checking your account...";

        return;
    }

    if (!currentUser) {
        memberMessage.textContent =
            "You must sign in first.";

        return;
    }

    const submitButton = form.querySelector(
        'button[type="submit"]'
    );

    submitButton.disabled = true;
    memberMessage.textContent = "Creating member...";

    const formData = new FormData(form);

    const membersReference = ref(
        database,
        `users/${currentUser.uid}/members`
    );

    const newMemberReference = push(membersReference);

    const member = {
        name: String(formData.get("name") ?? "").trim(),
        pronouns: String(
            formData.get("pronouns") ?? ""
        ).trim(),
        description: String(
            formData.get("description") ?? ""
        ).trim(),
        metadata: {
            color: String(
                formData.get("color") ?? "#af0000"
            )
        },
        archived: false
    };

    try {
        await set(newMemberReference, member);
        returnToMembers();
    } catch (error) {
        memberMessage.textContent =
            `Could not create member: ${error.message}`;

        submitButton.disabled = false;
    }
});