is_edit = false


function editRow(table_name, row_id, station_id) {
    // Заменяет элементы таблицы на веб формы 
    // и добавляет кнопку сохранения.
    // Paremetrs:
    // ---------
    // table_name : str
    //      Название таблицы, в строках которой нужно заменить элементы.
    // row_id : str
    //      Номер строки, элементы которой нужно заменить.
    // station_id : str, int
    //      Номер заправки, которая указана в таблице.
    //      Нужно для того, чтобы поставить эту заправке первой.
    if (table_name == "trans") {
        var table = document.querySelector(".table_workspace.trans")
        var form_names = [".date", ".odometer", ".station", ".gallons"]
    }
    else if (table_name == "fuel") {
        var table = document.querySelector(".table_workspace.fuel")
        var form_names = [".name", ".price"]
    }
    // Строка в которой была нажата кнопка
    var work_row = table.querySelector(".work_table_row.num_" + row_id)
    // Столбцы, в которых находятся веб формы
    var form_cols = work_row.querySelectorAll(".form_col")
    // Столбцы, в к содержутся значения(не веб формы)
    var table_cols = work_row.querySelectorAll(".table_col")
    // Названия и id заправок
    var fuel_data = document.querySelector(".index_container.navigation .form.names").querySelectorAll("option")

    form_cols[0].querySelector(".id").defaultValue = row_id
    for (var i = 1; i < form_cols.length - 1; i++) {
        form_cols[i].querySelector(form_names[i - 1]).defaultValue = table_cols[i - 1].innerHTML
        if (table_name == "trans") {
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
                    opt.value = fuel_data[t].value
                    opt.text = fuel_data[t].text
                    form_cols[i].querySelector(form_names[i - 1]).add(opt)
                }
            }
        }
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
    for (var i = 1; i < rows.length; i++) {
        rows[i].querySelector(".button.delete").style.display = "none"
        rows[i].querySelector(".button.edit").style.display = "none"
    }
}


function saveRow() {
    is_edit = false
}


function deleteRow(table_name, row_id) {
    var result = confirm("Удалить строку?")
    if (result) {
        var table = document.querySelector(".table_workspace." + table_name)
        table.querySelector(".work_table_row.num_" + row_id).querySelectorAll(".form_col")[0].querySelector(".id").value = row_id
        table.querySelector(".work_table_row.num_" + row_id).querySelectorAll(".form_col")[0].querySelector(".id").defaultValue = row_id
    }
}


function newRow(table_name) {
    if (is_edit) {
        alert("Сохраните редактируемую строку!")
    }
    else {
        // Строка где лежат формы для создания новой строки
        var row = document.querySelector(".table_workspace." + table_name + " .work_table_row.new")
        // Формы из полученной строки
        var form_cols = row.querySelectorAll(".form_col")
        // Данные о заправке, нужны для оптиций в select теге
        var fuel_data = document.querySelector(".index_container.navigation .form.names").querySelectorAll("option")
        
        for (var i = 0; i < form_cols.length; i++) {
            form_cols[i].style.display = "table-cell"
        }
        if (table_name == "trans") {
            for (var i = 0; i < fuel_data.length; i++) {
                var opt = document.createElement("option")
                opt.value = fuel_data[i].value
                opt.text = fuel_data[i].text
                form_cols[2].querySelector(".station").add(opt)
            }
        }
        is_edit = true
        hide_buttons()
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

    document.querySelector(".button." + tables[0]).style.borderColor = "#009933"
    document.querySelector(".button." + tables[0]).style.borderWidth = "3px"
    document.querySelector(".button." + tables[1]).style.borderColor = "#2b2b73"
    document.querySelector(".button." + tables[1]).style.borderWidth = "2px"
    document.querySelector(".table_name").value = table_name
    document.querySelector(".table_name").defaultValue = table_name
    console.log(document.querySelector(".table_name").value)
}

changeTable(document.querySelector(".table_name").innerHTML)