"use strict";

const dbg = false;

const loginForm = document.querySelector("#loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", validateLogin);
}

const registerForm = document.querySelector("#registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", validateRegister);
}

const registerPassword = document.querySelector("#registerPassword");
if (registerPassword) {
    registerPassword.oninput = function (event) {
        registerRepeatPassword.setAttribute("pattern", event.target.value);
    };
}

const registerRepeatPassword = document.querySelector(
    "#registerRepeatPassword"
);
if (registerRepeatPassword) {
    registerRepeatPassword.oninput = function (event) {
        if (event.target.validity.patternMismatch) {
            event.target.setCustomValidity("Пароли должны совпадать");
        } else {
            event.target.setCustomValidity("");
        }
    };
}

function validateLogin(evt) {
    evt.preventDefault();

    let email = loginForm.loginEmail.value;
    let password = loginForm.loginPassword.value;
    let enc_password = md5(password);

    if (dbg) {
        console.log("Form data:", first_name, last_name, email, password);
        console.log("Sended data:", first_name, last_name, email, enc_password);
    }

    auth_me(email, password);
    // auth_me(email, enc_password);
}

function validateRegister(evt) {
    evt.preventDefault();

    let first_name = registerForm.registerFirstName.value;
    let last_name = registerForm.registerLastName.value;
    let email = registerForm.registerEmail.value;
    let password = registerForm.registerPassword.value;
    let enc_password = md5(password);

    if (dbg) {
        console.log("Form data:", first_name, last_name, email, password);
        console.log("Sended data:", first_name, last_name, email, enc_password);
    }

    register_me(first_name, last_name, email, password);
    // register_me(first_name, last_name, email, enc_password);
}

function auth_me(email, password) {
    toggleSubmitSpinner(loginForm);

    let auth_data = { email: email, password: password };

    axios
        .post("/api/auth/login", auth_data)
        .then(function (response) {
            toggleSubmitSpinner(loginForm);
            showAlert({ message: response.data.message, type: "success" });

            window.location.href = loginForm.dataset.redirectTarget;
        })
        .catch(function (error) {
            toggleSubmitSpinner(loginForm);
            showAlert({ message: error.response.data.message, type: "danger" });
        });
}

function register_me(first_name, last_name, email, password) {
    toggleSubmitSpinner(registerForm);

    let register_data = { first_name: first_name, last_name: last_name, email: email, password: password };

    axios
        .post("/api/auth/register", register_data)
        .then(function (response) {
            toggleSubmitSpinner(registerForm);

            if (response.data.status == "success") {
                showAlert({ message: response.data.message, type: "success" });

                window.location.href = registerForm.dataset.redirectTarget;
            } else {
                showAlert({ message: response.data.message, type: "danger" });
            }
        })
        .catch(function (error) {
            toggleSubmitSpinner(registerForm);
            showAlert({ message: error.response.data.message, type: "danger" });
        });
}
