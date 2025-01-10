let table = document.getElementById('users')

document.querySelectorAll('.edit-user').forEach((item) => {
    item.onclick = edit_user
})

function edit_user(event) {
    let row = this.parentElement.parentElement
    let id = row.cells[1].textContent
    let username = row.cells[2]
    let password = row.cells[3]

    if (this.classList.value.includes('select-edit')) {
        username.contentEditable = false
        password.contentEditable = false
        this.classList.remove('select-edit')
        username.classList.remove('select-edit-cell')
        password.classList.remove('select-edit-cell')

        fetch('/update_user_name', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({'user_id': id, 'username': username.textContent, 'password': password.textContent}),
                mode: 'no-cors'})
        .then(response => response.json())
        .then(data => {console.log(data)})
        password.textContent = "***"
    }
    else {
        this.classList.add('select-edit')
        username.contentEditable = true
        password.contentEditable = true
        username.classList.add('select-edit-cell')
        password.classList.add('select-edit-cell')
        username.focus()
    }
}

document.getElementsByClassName('select-all-user')[0].onclick = select_all_row
function select_all_row(event) {
    let value = this.checked

    document.querySelectorAll('.select-user').forEach((item) => {
        item.checked = value
    })
}

document.getElementsByClassName('del-user')[0].addEventListener('click', () => {
    let data = {'user_id': [], 'row': []}
    let string_username = ""
    let flag = false
    document.querySelectorAll('.select-user').forEach((item) => {
        if (item.checked) {
            let row = item.parentElement.parentElement
            let user_id = row.cells[1].textContent
            let username = row.cells[2].textContent

            data['user_id'].push(user_id)
            data['row'].push(row)
            string_username += username + ', '
            flag = true
        }
    })
    if (flag) {
        let res = confirm('Уверены что хотите удалить пользователя ' + string_username + '?')
        if (res) {
            data['row'].forEach((row) => {row.parentElement.removeChild(row)})
            data['user_id'].forEach((user_id) => {
                fetch('/del_user', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({'user_id': user_id}),
                mode: 'no-cors'})
                .then(response => response.json())
                .then(data => {console.log(data)})
            })
        }
    }
})


document.getElementById('del-admin').addEventListener('click', () => {
    let res = confirm('Уверены, что хотите удалить текущего Admin?')
    if (res) {
        fetch('/del_admin', {method: "POST"})
    }
})