function editRow(row_id=0) {
    let form_cols = document.querySelectorAll(".work_form_col.row_" + row_id)
    let table_cols = document.querySelectorAll(".work_table_col.row_" + row_id)
    for (let i = 0; i < 4; i++) {
        form_cols[i].style.display = "table-cell"
        table_cols[i].style.display = "none"
    }    
}