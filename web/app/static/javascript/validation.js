// Проверка форм во время ввода данных


function validDateForm(date_form) {
    // Проверка введенной даты взависимости от введенного пробега.
    // Введеная дата должна быть больше, чем самая большая дата,
    // у которой пробег меньше, введенного нами.
    // Введеная дата должна быть меньше, чем самая минимальная дата,
    // у которой пробег больше, введенного нами
    let odometer_value = date_form.parentElement.parentElement.querySelector(".odometer").value
    if (odometer_value != "") {
        odometer_value = parseInt(odometer_value)
        let max_value = ""
        let min_value = ""
        let errors = []
        rows = document.querySelectorAll(".table_workspace.trans .work_table_row")
        for (let i = 1; i < rows.length; i++) {
            table_cols = rows[i].querySelectorAll(".table_col")
            if (parseInt(table_cols[1].innerHTML) < odometer_value && table_cols[0].innerHTML > min_value) {
                min_value = table_cols[0].innerHTML
            }
            else if (parseInt(table_cols[1].innerHTML) > odometer_value) {
                max_value = table_cols[0].innerHTML
                break
            }
        }
        if (min_value != "" && date_form.value < min_value) {
            errors.push("Date must be more or equal " + min_value)
        }
        if (max_value != "" && date_form.value > max_value) {
            errors.push("Date must be less or equal " + max_value)
        }
        document.querySelector(".error.table_row").innerHTML = ""
        if (errors.length != 0) {
            for (let i = 0; i < errors.length; i++) {
                document.querySelector(".error.table_row").innerHTML = "* " + errors[i] + "\n"
                date_form.style.borderColor = "red"
            }
            return
        }
        date_form.style.borderColor = "green"
    }
}


function validOdometerForm(odometer_form) {
    // Проверка введенного пробега, взависимости от введенной даты.
    // Введнный пробег должен отличаться от уже имеющихся пробегов.
    // А такж, если дата уже была введена, то пробег должен бьть:
    //  больше, чем пробег в предыдущей дате и 
    //  меньше чем пробег в следующей дате.
    let date_value = odometer_form.parentElement.parentElement.querySelector(".date").value
    let max_value = 0
    let min_value = 0
    let errors = []
    rows = document.querySelectorAll(".table_workspace.trans .work_table_row")
    for (let i = 1; i < rows.length; i++) {
        let table_cols = rows[i].querySelectorAll(".table_col")
        if (date_value != table_cols[0].innerHTML && odometer_form.value == table_cols[1].innerHTML) {
            errors.push("Odometer must be different from the existing one")
            break
        }
        if (table_cols[0].innerHTML < date_value && (parseInt(table_cols[1].innerHTML) > min_value || min_value == 0)) {
            min_value = (parseInt(table_cols[1].innerHTML))
        }
        else if (table_cols[0].innerHTML > date_value) {
            max_value = table_cols[1].innerHTML
            break
        }
    }
    if (errors.length == 0) {
        if (max_value && odometer_form.value >= max_value) {
            errors.push("Odometer must be less than " + max_value)
        }
        if (min_value && odometer_form.value <= min_value) {
            errors.push("Odometer must be more than " + min_value)
        }
    }
    document.querySelector(".error.table_row").innerHTML = ""
    if (errors.length != 0) {
        for (let i = 0; i < errors.length; i++) {
            document.querySelector(".error.table_row").innerHTML = "* " + errors[i] + "\n"
            odometer_form.style.borderColor = "red"
        }
        return
    }
    odometer_form.style.borderColor = "green"
}


function validForm(form) {
    form.style.borderColor = "green"
}