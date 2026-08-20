// ======================================
// GET FORM
// ======================================

const form = document.getElementById("registerForm");

const message = document.getElementById("message");


// ======================================
// FORM SUBMIT
// ======================================

form.addEventListener("submit", function (event) {

    // Stop page refresh
    event.preventDefault();


    // ==================================
    // GET VALUES
    // ==================================

    const name =
        document.getElementById("name").value.trim();

    const username =
        document.getElementById("username").value.trim();

    const email =
        document.getElementById("email").value.trim();

    const mobile =
        document.getElementById("mobile").value.trim();

    const password =
        document.getElementById("password").value;

    const confirmPassword =
        document.getElementById("confirmPassword").value;

    const course =
        document.getElementById("course").value;

    const address =
        document.getElementById("address").value.trim();


    // ==================================
    // VALIDATION
    // ==================================

    if (name === "") {

        showError("Please enter your name.");

        return;
    }


    if (username === "") {

        showError("Please enter username.");

        return;
    }


    if (email === "") {

        showError("Please enter email.");

        return;
    }


    if (!email.includes("@")) {

        showError("Please enter a valid email.");

        return;
    }


    if (mobile === "") {

        showError("Please enter mobile number.");

        return;
    }


    if (password === "") {

        showError("Please enter password.");

        return;
    }


    if (password.length < 8) {

        showError(
            "Password must contain at least 8 characters."
        );

        return;
    }


    if (password !== confirmPassword) {

        showError(
            "Passwords do not match."
        );

        return;
    }


    if (course === "") {

        showError("Please select a course.");

        return;
    }


    if (address === "") {

        showError("Please enter your address.");

        return;
    }


    // ==================================
    // SEND DATA TO FLASK
    // ==================================

    fetch(
        "http://127.0.0.1:5000/register",
        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body: JSON.stringify({

                name: name,

                username: username,

                email: email,

                mobile: mobile,

                password: password,

                course: course,

                address: address

            })

        }
    )


    // ==================================
    // GET FLASK RESPONSE
    // ==================================

    .then(function (response) {

        return response.json();

    })


    // ==================================
    // SHOW RESULT
    // ==================================

    .then(function (data) {

        if (data.success) {

            showSuccess(
                data.message
            );


            // Clear form

            form.reset();


            // Go to login page

            setTimeout(function () {

                window.location.href =
                    "login.html";

            }, 1500);


        } else {

            showError(
                data.message
            );

        }

    })


    // ==================================
    // SERVER ERROR
    // ==================================

    .catch(function (error) {

        console.log(error);

        showError(
            "Server connection failed."
        );

    });

});


// ======================================
// ERROR FUNCTION
// ======================================

function showError(text) {

    message.style.color = "red";

    message.textContent = text;

}


// ======================================
// SUCCESS FUNCTION
// ======================================

function showSuccess(text) {

    message.style.color = "green";

    message.textContent = text;

}