function get_date() {
    const t = new Date()
    const y = t.getFullYear()
    const m = ('0' + (t.getMonth() + 1)).slice(-2)
    const d = ('0' + t.getDate()).slice(-2)
    const H = ('0' + t.getHours()).slice(-2)
    const M = ('0' + t.getMinutes()).slice(-2)
    const S = ('0' + t.getSeconds()).slice(-2)

    return `${y}-${m}-${d}_${H}-${M}-${S}`
}

function waitingKeypress(keys) {
    return new Promise((resolve) => {
        window.onKeyHandler = function (e) {
            console.log(e.keyCode);
            for (let i = 0; i < keys.length; i++) {
                if (e.keyCode === keys[i]) {
                    document.removeEventListener('keydown', window.onKeyHandler);
                    resolve(i);
                }
            }
        }
        document.addEventListener('keydown', window.onKeyHandler);
    });
}

function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function set_image(element, src) {
    return new Promise(resolve => {
        element.onload = function () {
            resolve();
        };
        element.src = src
    });
}


async function fetchPost(url, data) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    return response.text(); // parses JSON response into native JavaScript objects
}