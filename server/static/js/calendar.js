document.body.addEventListener('click', function (event) {
    if (event.target.matches('a[href]')) {
        chrome.tabs.create({url: event.target.href});
    }
});
function main_function(calendar) {
    function create_table() {
        for (let row = 0; row < cRows; row++) {
            let tr = document.createElement('tr')
            for (let col = 0; col < cCols; col++) {
                let td = document.createElement('td')

                let div_number_day = document.createElement('div')
                div_number_day.className = 'number-day'
                td.appendChild(div_number_day)

                let div_hour_day = document.createElement('div')
                div_hour_day.className = 'hour-day'
                td.appendChild(div_hour_day)

                tr.appendChild(td)
            }
            table.appendChild(tr)
        }
    }

    function clear_table() {
        for (let y = 0; y < cRows; y++) {
            for (let x = 0; x < cCols; x++) {
                let cell = table.rows[y].cells[x]
                cell.className = ''
                cell.children[0].textContent = ''
                cell.children[1].textContent = ''
                cell.children[0].style.border = 'none'
                cell.children[1].contentEditable =  'false'
            }
        }
    }

    function fill_mouth_table(data, number_day, number_mouth, year) {
        document.getElementById('now-name-mouth').textContent = lst_name_mouth[number_mouth]
        document.getElementById('now-year').textContent = year

        // Очистка ячеек
        clear_table()

        let lst_mouth = data[Number(number_mouth)]

        let y = 0;
        let total_minutes = 0;
        let flag_total_minutes = true
        for (let i = 0; i < lst_mouth.length; i++) {
            let [type_day, week_day, day, minutes] = lst_mouth[i]
            let date = new Date()
            if (change_year === date.getFullYear() && number_mouth === date.getMonth() && day === date.getDate() + 1) {
                flag_total_minutes = false
            }

            if (day !== 1.0 && week_day === 0) y += 1
            let cell = table.rows[y].cells[week_day]

            cell.children[0].textContent = day
            cell.children[1].textContent = minutes_to_hours(minutes)
            cell.children[1].contentEditable =  'true'
            cell.children[1].oninput = edit_cell
            cell.onwheel = edit_cell_wheel

            if (type_day === 0) cell.className = 'day-off'
            else if (type_day === 1) cell.className = 'day-on'

            if (flag_total_minutes) total_minutes += minutes
        }
        document.getElementById('total-hours').textContent = Math.floor(total_minutes / 60) + ":" + (total_minutes % 60).toString().padStart(2, '0')

        fetch('/get_my_hours', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({'user_id': user_id, 'mouth': change_mouth + 1, 'year': change_year}),
                mode: 'no-cors'})
        .then(response => response.json())
        .then(data => {
            document.getElementById('my-hours').textContent = data['hours'] + ":" + data['minutes'].toString().padStart(2, '0')
            let diff = hours_to_minutes(document.getElementById('total-hours').textContent) - hours_to_minutes(document.getElementById('my-hours').textContent)
            document.getElementById('diff').textContent = minutes_to_hours(diff)
        })

    }

    function check_cell_hour(cell) {
    //     Проверка ячейки на количество часов. Если кол-во часов равно 0, то она меняет класс на day-off
    //     cell - блок со значением часов
        let value = cell.textContent
        if (value === '' || value === '0') {
            cell.textContent = '0:00'
            check_cell_hour(cell)

        }
        else {
            let [hour, minutes] = value.split(':')
            let parent = cell.parentElement
            if (Number(hour) + Number(minutes) === 0) parent.className = 'day-off'
            else if (Number(hour) + Number(minutes) !== 0) parent.className = 'day-on'
        }
    }

    function edit_cell(event) {
        check_cell_hour(this)
    }

    function edit_cell_wheel(event) {
        let div_total_hours = document.getElementById('total-hours')
        let diff = document.getElementById('diff')
        let total_minutes = hours_to_minutes(div_total_hours.textContent)

        let minutes = hours_to_minutes(this.children[1].textContent)
        if (event.deltaY > 0 && minutes !== 0) {
            minutes -= 5
            div_total_hours.textContent = minutes_to_hours(total_minutes - 5)
            diff.textContent  = minutes_to_hours(hours_to_minutes(diff.textContent) - 5)
        }
        else {
            minutes += 5
            div_total_hours.textContent = minutes_to_hours(total_minutes + 5)
            diff.textContent  = minutes_to_hours(hours_to_minutes(diff.textContent) + 5)
        }
        this.children[1].textContent = minutes_to_hours(minutes)
        check_cell_hour(this.children[1])
    }

    function hours_to_minutes(value) {
        let [hour, minute] = value.split(':')
        return Number(hour) * 60 + Number(minute)
    }

    function minutes_to_hours(value) {
        if (value >= 0) {
            let hour = Math.floor(value/60)
            let minutes = value % 60
            return hour + ":" + minutes.toString().padStart(2, '0')
        }
        else {
            let hour = (Math.floor(value/60) + 1) * (-1)
            let minutes = value % 60 * (-1)
            return '-' + hour + ":" + minutes.toString().padStart(2, '0')
        }

    }

    function next_mouth(event) {
        update_calendar_user()
        change_mouth += 1
        if (change_mouth > 11) {
            change_mouth = 0
            change_year += 1
        }
        fill_mouth_table(calendar[change_year], 1, change_mouth, change_year)
    }

    function prev_mouth(event) {
        update_calendar_user()
        change_mouth -= 1
        if (change_mouth < 0) {
            change_mouth = 11
            change_year -= 1
        }
        fill_mouth_table(calendar[change_year], 1, change_mouth, change_year)
    }

    function update_calendar_user() {
        let change_list = []

        let counter = 0
        let flag_change = false
        for (let y = 0; y < cRows; y++) {
            for (let x = 0; x < cCols; x++) {
                let cell = table.rows[y].cells[x]
                let day = Number(cell.children[0].textContent)

                if (day) {
                    let [hour, minute] = cell.children[1].textContent.split(':')
                    let hours = Number(hour) * 60 + Number(minute)
                    if (calendar[change_year][change_mouth][counter][3] !== hours) {
                        let type_day = (hour > 0) ? 1 : 0
                        change_list.push({
                            'year': change_year,
                            'mouth': change_mouth,
                            'number_day': day,
                            'type_day': type_day,
                            'hour': hours})
                        flag_change = true
                    }
                counter += 1
                }
            }
        }

        if (flag_change) {
            fetch('/update_calendar_user', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({'user_id': user_id, 'data': change_list}),
                mode: 'no-cors'})
            .then(response => response.json())
            .then(data => {
                console.log(data['status'] )
                if (data['status'] === 'success') {
                    change_list.forEach((item) => {
                        let year = item['year']
                        let mouth = item['mouth']
                        let number_day = item['number_day']

                        calendar[year][mouth][number_day - 1][3] = item['hour']
                        calendar[year][mouth][number_day - 1][0] = item['type_day']

                        let block = document.getElementsByClassName('calendar')[0]
                        block.style.backgroundColor = 'rgba(92,253,119,0.2)'
                        setTimeout(() => {block.style.backgroundColor = 'white';}, 500);
                    })
                }

            })
            .catch(error => {console.error("Ошибка при отправке запроса:", error);});
        }
    }

    document.body.onmouseleave = update_calendar_user

    document.getElementById('prev-mouth').onclick = prev_mouth
    document.getElementById('next-mouth').onclick = next_mouth

    create_table()
    fill_mouth_table(
        calendar[change_year],
        now_day,
        now_mouth,
        now_year)
}

async function main() {
    await fetch('get_calendar/' + user_id)
        .then(response => response.json())
        .then(data_user_calendar => {
            main_function(data_user_calendar)
        })
}

let lst_week_day = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
let lst_name_mouth = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

let date = new Date()
let now_day = date.getDate()
let now_mouth = date.getMonth()
let change_mouth  = now_mouth
let now_year = date.getFullYear()
let change_year = now_year

let table = document.getElementById("table-number-day")
let cRows = 6
let cCols = 7

main()
