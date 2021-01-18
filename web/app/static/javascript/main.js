is_edit = false


function editRow(row_id, station_id) {
    // Строка в которой была нажата кнопка
    var work_row = document.querySelector(".work_table_row.num_" + row_id)
    // Столбцы, в которых находятся веб формы
    var form_cols = work_row.querySelectorAll(".form_col")
    // Столбцы, в к содержутся значения(не веб формы)
    var table_cols = work_row.querySelectorAll(".table_col")
    // Названия и id заправок
    var fuel_data = document.querySelector(".navig_form.names").querySelectorAll("option")

    var form_names = [".date", ".odometer", ".station", ".gallons"]

    form_cols[0].querySelector(".id").defaultValue = row_id
    for (var i = 1; i < form_cols.length - 1; i++) {
        form_cols[i].querySelector(form_names[i - 1]).defaultValue = table_cols[i - 1].innerHTML
        if (i == 3) {
            var option = document.createElement("option")
            option.value = station_id
            option.text = table_cols[i - 1].innerHTML
            form_cols[i].querySelector(form_names[i - 1]).add(option)
            for (var t = 0; t < fuel_data.length; t++) {
                var opt = document.createElement("option")
                if (fuel_data[t].value == station_id) {
                    continue
                }
                else {
                    opt.value = fuel_data[t].value
                    opt.text = fuel_data[t].text
                }
                form_cols[i].querySelector(form_names[i - 1]).add(opt)
            }
        }
        form_cols[i].querySelector(form_names[i - 1]).defaultValue = table_cols[i - 1].innerHTML
    }
    for (var i = 1; i < form_cols.length; i++) {
        form_cols[i].style.display = "table-cell"
        table_cols[i - 1].style.display = "none"
    }
    work_row.style.backgroundColor = "#808080"
    is_edit = true
    hide_buttons()
}


function hide_buttons() {
    var rows = null
    if (document.querySelector(".table_workspace.trans").style.display != "none") {
        rows = document.querySelectorAll(".table_workspace.trans .work_table_row")
    }
    if (document.querySelector(".table_workspace.fuel").style.display != "none") {
        rows = document.querySelectorAll(".table_workspace.fuel .work_table_row")
    }
    for (var i = 0; i < rows.length - 1; i++) {
        rows[i].querySelector(".button.delete").style.display = "none"
        rows[i].querySelector(".button.edit").style.display = "none"
    }
}


function saveRow() {
    is_edit = false
}


function deleteRow(row_id) {
    var result = confirm("Удалить строку?")
    if (result) {
        var table = null
        if (document.querySelector(".table_workspace.trans").style.display != "none") {
            table = document.querySelectorAll(".table_workspace.trans")
        }
        if (document.querySelector(".table_workspace.fuel").style.display != "none") {
            table = document.querySelectorAll(".table_workspace.fuel")
        }
        table.querySelector(".work_table_row.num_" + row_id).querySelectorAll(".form_col")[0].querySelector(".id").value = row_id
        table.querySelector(".work_table_row.num_" + row_id).querySelectorAll(".form_col")[0].querySelector(".id").defaultValue = row_id
    }
}


function newRow() {
    if (is_edit) {
        alert("Сохраните редактируемую строку!")
    }
    else {
        var row = null
        if (document.querySelector(".table_workspace.trans").style.display != "none") {
            var row = document.querySelector(".table_workspace.trans .work_table_row.new")
        }
        else if (document.querySelector(".table_workspace.fuel").style.display != "none") {
            var row = document.querySelector(".table_workspace.fuel .work_table_row.new")
        }
        var form_cols = row.querySelectorAll(".form_col")
        var fuel_data = document.querySelector(".navig_form.names").querySelectorAll("option")
        var table_col = row.querySelector(".table_col")

        table_col.style.display = "none"
        for (var i = 0; i < form_cols.length; i++) {
            form_cols[i].style.display = "table-cell"
        }

        for (var i = 0; i < fuel_data.length; i++) {
            var opt = document.createElement("option")
            opt.value = fuel_data[i].value
            opt.text = fuel_data[i].text
            form_cols[2].querySelector(".station").add(opt)
        }
        is_edit = true
        hide_buttons()
    }
}


function validDateNewRow(date) {
    var form_odometer = document.querySelector(".work_table_row.new .form_col .odometer").value
    if (form_odometer != "") {
        form_odometer = parseInt(form_odometer)
        var max_value = ""
        var min_value = ""
        var error = ""
        rows = document.querySelectorAll(".work_table_row")
        for (var i = 0; i < rows.length - 1; i++) {
            table_cols = rows[i].querySelectorAll(".table_col")
            if (parseInt(table_cols[1].innerHTML) < form_odometer && table_cols[0].innerHTML > min_value) {
                min_value = table_cols[0].innerHTML
            }
            if (parseInt(table_cols[1].innerHTML) > form_odometer) {
                max_value = table_cols[0].innerHTML
                break
            }
        }
        if (date.value <= min_value || date.value >= max_value) {
            error = "Date must be more than " + min_value + " and less than " + max_value
        }
        if (error != "") {
            document.querySelector(".error.new_row").innerHTML = "* " + error
            date.style.borderColor = "red"
        }
        else {
            document.querySelector(".error.new_row").innerHTML = ""
            date.style.borderColor = "green"
        }
    }
}


function validOdometerNewRow(odometer) {
    form_date = document.querySelector(".work_table_row.new .form_col .date").value
    var values = []
    var max_values = []
    var min_values = []
    var error = ""
    rows = document.querySelectorAll(".work_table_row")
    for (var i = 0; i < rows.length - 1; i++) {
        table_cols = rows[i].querySelectorAll(".table_col")
        if (odometer.value == table_cols[1].innerHTML) {
            error = "Odometer must be different from the existing one"
            break
        }
        if (form_date != "") {
            if (form_date == table_cols[0].innerHTML) {
                values.push(parseInt(table_cols[1].innerHTML))
            }
            else if (table_cols[0].innerHTML < form_date) {
                min_values.push(parseInt(table_cols[1].innerHTML))
            }
            else if (table_cols[0].innerHTML > form_date) {
                max_values.push(parseInt(table_cols[1].innerHTML))
            }
        }
    }
    if (error == "") {
        if (values.length == 1 && odometer.value == values[0]) {
            error = "Odometer must be more or less than " + values[0]
        }
        else if (values.length > 1 && (odometer.value <= Math.min.apply(null, values) || odometer.value >= Math.max.apply(null, values))) {
            error = "Odometer must be more than " + Math.min.apply(null, values) + " and less than " + Math.max.apply(null, values)
        }
        else if (odometer.value <= Math.max.apply(null, min_values) || odometer.value >= Math.min.apply(null, max_values)) {
            error = "Odometer must be more than " + Math.max.apply(null, min_values) + " and less than " + Math.min.apply(null, max_values)
        }
    }
    if (error != "") {
        document.querySelector(".error.new_row").innerHTML = "* " + error
        odometer.style.borderColor = "red"
    }
    else {
        document.querySelector(".error.new_row").innerHTML = ""
        odometer.style.borderColor = "green"
    }
}


function changeTable(table_name) {
    var tables = []
    if (table_name == "trans") {
        tables.push("trans")
        tables.push("fuel")
    }
    else {
        tables.push("fuel")
        tables.push("trans")
    }
    // Показываем таблицу с данными о транзакциях
    document.querySelector(".table_workspace." + tables[1]).style.display = "none"
    document.querySelector(".table_workspace." + tables[0]).style.display = "flex"

    // Показываем навигационную панель для транзакций
    document.querySelector(".navig_inner." + tables[1]).style.display = "none"
    document.querySelector(".navig_inner." + tables[0]).style.display = "block"

    document.querySelector(".navig_button." + tables[0]).backgroundColor = "#66ff66"
    document.querySelector(".navig_button." + tables[1]).backgroundColor = "#c7c7ea"
    document.querySelector(".table_name").value = table_name
    document.querySelector(".table_name").defaultValue = table_name
    console.log(document.querySelector(".table_name").value)
}

changeTable(document.querySelector(".table_name").value)