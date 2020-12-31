function editRow(row_id=0) {
    let form_cols = document.querySelectorAll(".work_form_col.row_" + row_id)
    let table_cols = document.querySelectorAll(".work_table_col.row_" + row_id)
    let form_names = [".date", ".odometer", ".station", ".gallons"]
    for (let i = 0; i < 4; i++) {
        if (i == 3) {
            let option = document.createElement("options")
            option.innerHTML = "Fuck"
            form_cols[i].querySelector(form_names[i]).appendChild(option)
        }
        else {
            form_cols[i].querySelector(form_names[i]).defaultValue = table_cols[i].innerHTML
        }
        form_cols[i].style.display = "table-cell"
        table_cols[i].style.display = "none"
    }
    

}