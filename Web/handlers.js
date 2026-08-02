import {
    auth,
    database,
    ref,
    set,
    onValue,
    remove,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "./server-auth.js";

const openBtn = document.getElementById("open");
const membersDiv = document.getElementById("members");
const createMemberBtn = document.getElementById("create_member");
const exportBtn = document.getElementById("export");

const authPanel = document.getElementById("auth-panel");
const authForm = document.getElementById("auth-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const createAccountBtn = document.getElementById("create-account");
const signOutBtn = document.getElementById("sign-out");
const authMessage = document.getElementById("auth-message");
const accountStatus = document.getElementById("account-status");
const appElement = document.getElementById("app");

let currentUser = null;
let currentMembers = {};
let stopMembersListener = null;

function getMembersPath(userUid) {
    return `users/${userUid}/members`;
}

function build(members) {
    membersDiv.replaceChildren();

    const memberEntries = Object.entries(members);

    if (memberEntries.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.className = "empty-message";
        emptyMessage.textContent = "You do not have any members yet.";

        membersDiv.appendChild(emptyMessage);
        return;
    }

    for (const [memberUid, memberData] of memberEntries) {
        const memberDiv = document.createElement("div");
        const actionsDiv = document.createElement("div");

        const memberName = document.createElement("h3");
        const memberPronouns = document.createElement("h5");
        const memberDescription = document.createElement("p");
        const removeMemberBtn = document.createElement("button");

        memberDiv.id = `${memberUid}-div`;
        memberDiv.className = "member";

        actionsDiv.className = "action";

        memberName.textContent = memberData.name ?? "Unnamed member";
        memberPronouns.textContent = memberData.pronouns ?? "";
        memberDescription.textContent = memberData.description ?? "";

        removeMemberBtn.textContent = "Remove member";
        removeMemberBtn.type = "button";

        const memberColor =
            memberData.metadata?.color ?? "#6400de";

        memberDiv.style.background =
            `linear-gradient(to left, #202020, ${memberColor}50)`;

        memberDiv.appendChild(memberName);

        if (memberPronouns.textContent !== "") {
            memberDiv.appendChild(memberPronouns);
        }

        if (memberDescription.textContent !== "") {
            memberDiv.appendChild(memberDescription);
        }

        removeMemberBtn.addEventListener("click", async function () {
            if (!currentUser) {
                return;
            }

            const confirmed = window.confirm(
                `Remove ${memberName.textContent}?`
            );

            if (!confirmed) {
                return;
            }

            try {
                await remove(
                    ref(
                        database,
                        `${getMembersPath(currentUser.uid)}/${memberUid}`
                    )
                );
            } catch (error) {
                window.alert(
                    `Could not remove member: ${error.message}`
                );
            }
        });

        actionsDiv.appendChild(removeMemberBtn);
        memberDiv.appendChild(actionsDiv);
        membersDiv.appendChild(memberDiv);
    }
}

function downloadJSON(data, filename = "members.json") {
    const jsonText = JSON.stringify(data, null, 4);

    const blob = new Blob(
        [jsonText],
        {
            type: "application/json"
        }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = filename;

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
}

function showAuthMessage(message, isError = false) {
    authMessage.textContent = message;
    authMessage.classList.toggle("error", isError);
}

function startMembersListener(user) {
    if (stopMembersListener) {
        stopMembersListener();
        stopMembersListener = null;
    }

    const membersReference = ref(
        database,
        getMembersPath(user.uid)
    );

    stopMembersListener = onValue(
        membersReference,
        function (snapshot) {
            currentMembers = snapshot.val() ?? {};
            build(currentMembers);
        },
        function (error) {
            membersDiv.textContent =
                `Could not load members: ${error.message}`;
        }
    );
}

authForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    showAuthMessage("Signing in...");

    try {
        await signInWithEmailAndPassword(
            auth,
            emailInput.value.trim(),
            passwordInput.value
        );

        authForm.reset();
        showAuthMessage("");
    } catch (error) {
        showAuthMessage(error.message, true);
    }
});

createAccountBtn.addEventListener("click", async function () {
    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!email || !password) {
        showAuthMessage(
            "Enter an email and password first.",
            true
        );

        return;
    }

    showAuthMessage("Creating account...");

    try {
        await createUserWithEmailAndPassword(
            auth,
            email,
            password
        );

        authForm.reset();
        showAuthMessage("");
    } catch (error) {
        showAuthMessage(error.message, true);
    }
});

signOutBtn.addEventListener("click", async function () {
    try {
        await signOut(auth);
    } catch (error) {
        window.alert(`Could not sign out: ${error.message}`);
    }
});

onAuthStateChanged(auth, function (user) {
    currentUser = user;

    if (!user) {
        if (stopMembersListener) {
            stopMembersListener();
            stopMembersListener = null;
        }

        currentMembers = {};
        build({});

        authPanel.hidden = false;
        appElement.hidden = true;
        signOutBtn.hidden = true;

        accountStatus.textContent = "Not signed in";
        return;
    }

    authPanel.hidden = true;
    appElement.hidden = false;
    signOutBtn.hidden = false;

    accountStatus.textContent =
        user.email ?? user.uid;

    startMembersListener(user);
});

openBtn.addEventListener("change", async function () {
    if (!currentUser) {
        return;
    }

    const file = openBtn.files?.[0];

    if (!file) {
        return;
    }

    try {
        const fileText = await file.text();
        const importedMembers = JSON.parse(fileText);

        if (
            importedMembers === null ||
            typeof importedMembers !== "object" ||
            Array.isArray(importedMembers)
        ) {
            throw new Error(
                "The JSON file must contain a member object."
            );
        }

        await set(
            ref(
                database,
                getMembersPath(currentUser.uid)
            ),
            importedMembers
        );

        openBtn.value = "";
    } catch (error) {
        window.alert(
            `Could not import members: ${error.message}`
        );

        openBtn.value = "";
    }
});

createMemberBtn.addEventListener("click", function () {
    if (!currentUser) {
        return;
    }

    const createMemberUrl = "createmember.html";
    const isMobile =
        window.matchMedia("(max-width: 600px)").matches;

    if (isMobile) {
        window.location.href = createMemberUrl;
        return;
    }

    const createMemberWindow = window.open(
        createMemberUrl,
        "createMember",
        "width=500,height=600"
    );

    if (!createMemberWindow) {
        window.location.href = createMemberUrl;
    }
});

exportBtn.addEventListener("click", function () {
    if (!currentUser) {
        return;
    }

    downloadJSON(
        currentMembers,
        "members.json"
    );
});