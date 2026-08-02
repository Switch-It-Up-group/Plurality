import { initializeApp } from "https://www.gstatic.com/firebasejs/12.17.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.17.0/firebase-analytics.js";

import {
    getAuth,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.17.0/firebase-auth.js";

import {
    getDatabase,
    ref,
    set,
    push,
    onValue,
    remove,
    update
} from "https://www.gstatic.com/firebasejs/12.17.0/firebase-database.js";

const firebaseConfig = {
    apiKey: "AIzaSyDpya_ncU9w7RqaoZK3IZd3xfmUM7tZKBk",
    authDomain: "siu-auth.firebaseapp.com",
    projectId: "siu-auth",
    storageBucket: "siu-auth.firebasestorage.app",
    messagingSenderId: "303004907259",
    appId: "1:303004907259:web:28e32c27f9c4a06474225e",
    measurementId: "G-82WH19C7SD",
    databaseURL: "https://siu-auth-default-rtdb.firebaseio.com/"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const database = getDatabase(app);

export {
    app,
    analytics,
    auth,
    database,
    ref,
    set,
    push,
    onValue,
    remove,
    update,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
};