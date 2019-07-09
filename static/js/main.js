/**
 * Inicializa a página principal. Deve ser carregado no html
 * @module main.js
 */

// import * as util from "./common/util.js";

document.getElementById("btn_add_row").addEventListener("click", event => {
    event.preventDefault();

    const body = document.getElementById("table1_body");
    const row = body.insertRow(-1);
    const cell_x = row.insertCell(0);
    const cell_y = row.insertCell(1);
    const cell_yerr = row.insertCell(2);
    const cell_delete = row.insertCell(3);

    // cell_x.setAttribute("contenteditable", true);
    // cell_y.setAttribute("contenteditable", true);
    // cell_yerr.setAttribute("contenteditable", true);
    cell_delete.setAttribute("name", "delete_row");

    cell_x.innerHTML = `<input type="number"/>`;
    cell_y.innerHTML = `<input type="number"/>`;
    cell_yerr.innerHTML = `<input type="number"/>`;

    const child = `
        <button
            id="btn_remove_row${row.rowIndex}"
            class="btn waves-effect waves-light red darken-3"
        >
            <i class="material-icons">delete_forever</i>
        </button>
    `;

    cell_delete.insertAdjacentHTML("beforeend", child);

    const button = document.getElementById(`btn_remove_row${row.rowIndex}`);

    button.addEventListener("click", () => {
        body.deleteRow(row.rowIndex - 1);
    });
});
