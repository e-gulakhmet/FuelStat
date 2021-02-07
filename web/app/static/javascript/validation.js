// Проверка форм во время ввода данных


function validDateForm(date_form) {
    // Проверка введенной даты взависимости от введенного пробега.
    // Введеная дата должна быть больше, чем самая большая дата,
    // у которой пробег меньше, введенного нами.
    // Введеная дата должна быть меньше, чем самая минимальная дата,
    // у которой пробег больше, введенного нами
    odometer_value = date_form.parentElement.parentElement.querySelector(".odometer").value
    if (odometer_value != "") {
        odometer_value = parseInt(odometer_value)
        var max_value = ""
        var min_value = ""
        var error = ""
        rows = document.querySelectorAll(".table_workspace.trans .work_table_row")
        console.log(rows)
        for (var i = 1; i < rows.length - 1; i++) {
            table_cols = rows[i].querySelectorAll(".table_col")
            if (parseInt(table_cols[1].innerHTML) < odometer_value && table_cols[0].innerHTML > min_value) {
                min_value = table_cols[0].innerHTML
            }
            if (parseInt(table_cols[1].innerHTML) > odometer_value) {
                max_value = table_cols[0].innerHTML
                break
            }
        }
        if (date_form.value <= min_value || date_form.value >= max_value) {
            error = "Date must be more than " + min_value + " and less than " + max_value
        }
        if (error != "") {
            document.querySelector(".error.new_row").innerHTML = "* " + error
            date_form.style.borderColor = "red"
        }
        else {
            document.querySelector(".error.new_row").innerHTML = ""
            date_form.style.borderColor = "green"
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