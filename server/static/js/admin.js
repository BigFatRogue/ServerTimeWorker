let table = document.getElementById('users')

document.querySelectorAll('.edit-user').forEach((item) => {
    item.onclick = edit_user
})

function edit_user(event) {
    let row = this.parentElement.parentElement
    let id = row.cells[1].textContent
    let username = row.cells[2]

    if (this.classList.value.includes('select-edit')) {
        username.contentEditable = false
        this.classList.remove('select-edit')
        username.classList.remove('select-edit-cell')

        fetch('/update_user_name', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({'user_id': id, 'username': username.textContent}),
                mode: 'no-cors'})
        .then(response => response.json())
        .then(data => {console.log(data)})
    }
    else {
        this.classList.add('select-edit')
        username.contentEditable = true
        username.classList.add('select-edit-cell')
        username.focus()
    }
}

document.getElementById('select-all-user').onclick = select_all_row
function select_all_row(event) {
    let value = this.checked

    document.querySelectorAll('#select-user').forEach((item) => {
        item.checked = value
    })
}

document.querySelectorAll('.del-user').forEach((item) => {
    item.onclick = del_user
})

function del_user(event) {
    let row = this.parentElement.parentElement
    let username = row.cells[2].textContent

    let res = confirm('Уверены что хотите удалить пользователя ' + username + '?')
    if (res) {
        let id = row.cells[1].textContent
        row.parentElement.removeChild(row)

        fetch('/del_user', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({'user_id': id}),
                mode: 'no-cors'})
        .then(response => response.json())
        .then(data => {console.log(data)})
    }
}