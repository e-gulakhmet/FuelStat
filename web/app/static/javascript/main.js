is_edit = false

function editRow(row_id, station_id) {
    var work_row = document.querySelector(".work_table_row.num_" + row_id)
    var form_cols = work_row.querySelectorAll(".form_col")
    var table_cols = work_row.querySelectorAll(".table_col")
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
                if ( fuel_data[t].value == station_id) {
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
    rows = document.querySelectorAll(".work_table_row")
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
        document.querySelector(".work_table_row.num_" + row_id).querySelectorAll(".form_col")[0].querySelector(".id").value = row_id
        document.querySelector(".work_table_row.num_" + row_id).querySelectorAll(".form_col")[0].querySelector(".id").defaultValue = row_id
    }
}


function newRow() {
    if (is_edit) {
        alert("Сохраните редактируемую строку!")
    }
    else {
        var row = document.querySelector(".work_table_row.new")
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