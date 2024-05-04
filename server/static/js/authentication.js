let div_reg = document.getElementById("registration")
let div_auth = document.getElementById("authentication")
let tab_right = document.getElementById('tab-right')
let tab_left = document.getElementById('tab-left')

if (page === 'reg') {
    div_reg.style.display = "block";
    div_auth.style.display = "none";
    tab_right.className += ' active'
}
else {
    div_auth.style.display = "block";
    div_reg.style.display = "none";
    tab_left.className += ' active'
}

function open_tab(event, log) {
    let tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tab-links");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(log).style.display = "block";
    event.currentTarget.className += " active";
}

document.onkeydown = function(event){
    if (event.ctrlKey && event.shiftKey && event.key === "A") {
        document.location.href = '/admin'
    }

}