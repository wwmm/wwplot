/**
 * Inicializa a página principal. Deve ser carregado no html
 * @module main.js
 */

import * as util from "./common/util.js";

document.getElementById("btn_add_row").addEventListener("click", event => {
    event.preventDefault();

    const table = document.getElementById("table1");
    const nrows = table.rows.length;

    const row = table.insertRow(nrows);

    const cell_x = row.insertCell(0);
    const cell_y = row.insertCell(1);
    const cell_yerr = row.insertCell(2);

    cell_x.setAttribute("contenteditable", true);
    cell_y.setAttribute("contenteditable", true);
    cell_yerr.setAttribute("contenteditable", true);

    cell_x.innerHTML = "0";
    cell_y.innerHTML = "0";
    cell_yerr.innerHTML = "0";
});
