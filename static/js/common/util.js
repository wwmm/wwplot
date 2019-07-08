/**
 * Verifica se uma string está vazia
 * @param {string} str
 * @return boolean
 */
export function isEmpty(str) {
    return !str || 0 === str.length;
}

/**
 * Remove os widgets filhos do widget dado como argumento
 * @param {*} node
 */
export function remove_children(node) {
    while (node.firstChild != null) {
        node.removeChild(node.lastChild);
    }
}

/**
 * Popula um select com os elementos do array dado como entrada
 * @param {*} label
 * @param {Array<string>} list
 * @param {*} select
 */
export function add_list_to_select(list, select) {
    let children = "";

    for (let i = 0; i < list.length; i++) {
        if (!isEmpty(list[i])) {
            children = children.concat(`    <option value="${list[i]}">${list[i]}</option>`);
        }
    }

    select.insertAdjacentHTML("beforeend", children);

    M.FormSelect.init(select);
}

/**
 * Popula uma tabela com as componentes do array de entrada
 * @param {Array<string>} list
 * @param {*} out_widget
 */
export function add_list_to_tbody(list, out_widget) {
    let children = "";

    // colunas
    for (let i = 0; i < list.length; i++) {
        if (!isEmpty(list[i])) {
            let params = list[i].split(",");

            children = children.concat("<tr>");

            // linhas
            for (let j = 0; j < params.length; j++) {
                children = children.concat(`    <td>${params[j]}</td>`);
            }

            children = children.concat("</tr>");
        }
    }

    out_widget.insertAdjacentHTML("beforeend", children);
}

/**
 * Popula um collection do materializecss com os elementos do array de entrada
 * @param {Array<string>} list
 * @param {*} out_widget
 */
export function add_list_to_collection(list, out_widget) {
    let children = "";

    for (let i = 0; i < list.length; i++) {
        if (!isEmpty(list[i])) {
            children = children.concat(`<li class="collection-item left-align">${list[i]}</li>`);
        }
    }

    out_widget.insertAdjacentHTML("beforeend", children);
}

/**
 * Mostra para o cliente um toast com uma mensagem sobre o status de uma operação
 * @param {string} msg
 */
export function feedback(msg) {
    M.toast({
        html: `
        <div class="card red darken-4 center">
            <div class="card-content">
                <span class="white-text">${msg}</span>
            </div>
        </div>
        `,
        displayLength: 2000
    });
}

export function remove_element_select(select, value) {
    for (let n = 0; n < select.length; n++) {
        if (select.options[n].text === value) {
            select.remove(n);
            M.FormSelect.init(select);
            break;
        }
    }
}

/**
 * Usada apenas para debug. Imprime o conteúdo de uma FormData no console
 * @param {object} data
 */
export function print_formdata(data) {
    for (let p of data.entries()) {
        console.log(p);
    }
}
