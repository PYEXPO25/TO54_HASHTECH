import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-auth.js";

const firebaseConfig = {
            apiKey: "AIzaSyCBpNlGS0Zg7SyVa2ZzQ_Vv_xr0QUKUivA",
            authDomain: "test-patient-19648.firebaseapp.com",
            projectId: "test-patient-19648",
            storageBucket: "test-patient-19648.firebasestorage.app",
            messagingSenderId: "980312131670",
            appId: "1:980312131670:web:48fc6b26b95b25ce3453f7"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);


function login() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (email === "" || password === "") {
        alert("Please fill in all fields.");
        return;
    }

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            alert("Login Successful!");
            window.location.href = "dashboard.html";
        })
        .catch(error => alert(error.message));
}

function signup() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (email === "" || password === "") {
        alert("Please fill in all fields.");
        return;
    }

    createUserWithEmailAndPassword(auth, email, password)
        .then(() => {
            alert("Signup Successful!");
            window.location.href = "login4.html";
        })
        .catch(error => alert(error.message));
}

function togglePassword() {
    const passwordField = document.getElementById("password");
    passwordField.type = passwordField.type === "password" ? "text" : "password";
}

var loginButton=document.getElementById('login-button');
if(loginButton){
    loginButton.addEventListener("click", function() {login();return false;});
}

var createButton=document.getElementById('create-account');
if(createButton){
    createButton.addEventListener("click", function() {signup();return false;});
}

var signupButton=document.getElementById('signup-button');
if(signupButton){    
    signupButton.addEventListener("click", function() {window.location.href = "fsign.html";});
}