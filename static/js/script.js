/**
* Interact with Flask for getting organism names matching at least 3 character 
of the input form for organism name
*/
function setupAutocomplete() {
    const organismInput = document.getElementById('organism-input');
    
    if (!organismInput) {
        console.error("Elemento con id 'organism-input' non trovato.");
        return;
    }

    organismInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length >= 3) {
            fetch(`/phylorna/search/search_organisms?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    const datalist = document.getElementById('organism-list');
                    datalist.innerHTML = ''; // Svuota il menu a tendina
                    data.forEach(organism => {
                        const option = document.createElement('option');
                        option.value = organism;
                        datalist.appendChild(option);
                    });
                })
                .catch(error => console.error("Errore nel caricamento dei dati:", error));
        }
    });
}


/**
 * If the user selects a taxon rank, enable the taxon dropdown menu
 * @param rank - the select box where the user can select a taxon rank
 */
function check_taxon_rank(rank){
    document.getElementById("Taxon_id").disabled = rank.value === '';
}


/**
 * Returns a string with all the formats chosen by the client, if none then returns null.
 * @returns {string|null}
 */
function check_format_dl(){
    var check_button_format = document.getElementsByClassName("check_button_format");
    var formats_string = '';
    var header;
    var isSelected = false;
    if(document.getElementById("header").checked === true) {
        header = document.getElementById("header").value;
    } else {
         header = document.getElementById("n_header").value;
    }
    for(var i = 0; i < check_button_format.length; i++) {
        if(check_button_format[i].checked === true){
            formats_string = header + check_button_format[i].value + "," + formats_string;
            isSelected = true;
        }
    }
    if(isSelected){
        return formats_string;
    }else {
        return null;
    }
}


/**
 * Returns the taxonomy chosen by the client
 * @returns {string}
 */
function check_taxonomy_dl(){
    var check_buttons_taxonomy = document.getElementsByClassName("check_button_taxonomy")
    var taxonomy_string = '';
    for(var i = 0; i < check_buttons_taxonomy.length; i++) {
        if(check_buttons_taxonomy[i].checked === true){
            taxonomy_string = check_buttons_taxonomy[i].value + "," + taxonomy_string;
        }
    }
    return  taxonomy_string;
}


/**
 * Makes an ajax call to download the csv with all the rna sequences chosen by the client.
 */
async function download_csv_from_db() {
    const all_ref_ids = rows_selected;
    const taxonomy = check_taxonomy_dl();
    const jsonData = JSON.stringify({filenames: all_ref_ids, taxonomy: taxonomy});
    return $.ajax({
        url: '/phylorna/download_files_csv',
        type: 'POST',
        data: jsonData,
        contentType: 'application/json',
        xhrFields:{
            responseType: 'blob'
        }
    }).then(function(data) {
            let date = new Date().toJSON();
            let filename = date.concat(".csv")
            saveAs(data, filename);
    });
}


/**
 * Retrieves the selected rows from the table, checks for the desired file format(s) to download, and sends a request
 *to the server to download the selected files in a ZIP archive. If the download is successful, it prompts the user to save the ZIP
 *archive with a filename consisting of the current date and time.
 */
/**
function download_file_from_db() {
    var all_ref_ids = rows_selected;
    var formats = check_format_dl();
    if(formats === null){
        return;
    }
    var jsonData = JSON.stringify({filenames: all_ref_ids, formats: formats});
    $.ajax({
        url: '/phylorna/download_files',
        type: 'POST',
        data: jsonData,
        contentType: 'application/json',
        xhrFields:{
            responseType: 'blob'
        },
        success: function(data) {
            let date = new Date().toJSON();
            let filename = date.concat(".zip")
            saveAs(data, filename);
        }
    });
}
*/

/**
 * Retrieves the selected rows from the table, checks for the desired file format(s) to download, 
 * and sends a request to the server to download the selected files in a ZIP archive. 
 * If the download is successful, it prompts the user to save the ZIP archive with a filename consisting of the current date and time.
 */

/** function download_file_from_db() {
    var all_ref_ids = rows_selected;
    var formats = check_format_dl();
    if (formats === null) {
        return;
    }

    var jsonData = JSON.stringify({filenames: all_ref_ids, formats: formats});
    var progress_bar = document.getElementById("download-progress");

    // Reset progress bar
    progress_bar.value = 0;

    // Set up a timer for simulating progress based on the number of files
    var timer = (all_ref_ids.length / 10) * 2000; // Adjust the timing as needed
    var interval = setInterval(function () {
        progress_bar.value += 10;
        if (progress_bar.value >= 100) {
            clearInterval(interval);
        }
    }, timer / 10);

    $.ajax({
        url: '/phylorna/download_files',
        type: 'POST',
        data: jsonData,
        contentType: 'application/json',
        xhrFields: {
            responseType: 'blob'
        },
        success: function (data) {
            let date = new Date().toJSON();
            let filename = date.concat(".zip");
            saveAs(data, filename);

            // Reset progress bar on completion
            progress_bar.value = 0;
            clearInterval(interval);
        },
        error: function () {
            clearInterval(interval);
            progress_bar.value = 0;
            alert("An error occurred while downloading the file.");
        }
    });
}
*/

function download_file_from_db() {
    var all_ref_ids = rows_selected; // Assume `rows_selected` è definito correttamente
    var formats = check_format_dl(); // Assume `check_format_dl` è definito correttamente

    if (formats === null) {
        alert("Select at least a format!");
        return; // Esci se non sono selezionati formati
    }

    var jsonData = JSON.stringify({ filenames: all_ref_ids, formats: formats });

    return $.ajax({
        url: '/phylorna/download_files',
        type: 'POST',
        data: jsonData,
        contentType: 'application/json',
        xhrFields: {
            responseType: 'blob' // Per gestire i dati binari
        }
    }).then(function (data, textStatus, xhr) {
        // Estrai il nome del file dall'intestazione della risposta, se presente
        var disposition = xhr.getResponseHeader('Content-Disposition');
        var date = new Date().toJSON();
        var filename = date.concat(".zip")

        //var filename = "download.zip"; // Nome predefinito

        if (disposition && disposition.indexOf('attachment') !== -1) {
            var matches = /filename="(.+)"/.exec(disposition);
            if (matches && matches[1]) {
                filename = matches[1];
            }
        }

        // Salva il file usando FileSaver.js
        saveAs(data, filename);
        return true;
    }).catch(function (xhr, status, error) {
        alert("Error during download: " + error);
        return false;
    });
}

/**
 * It calls two functions that download CSV and addictional files
 */
function final_download(resetSelected = false){
    if (!confirm('Are you sure you want to download csv and zip files? Large selections may take some time to download, please wait until both the downloads are activated\n')) {
        return;
    }
    showOverlay()
    // Gestione asincrona
    Promise.all([
        download_csv_from_db(),
        download_file_from_db()
    ])
    .then(() => {
        // Nascondi spinner quando TUTTO è finito
        hideOverlay();
        if (resetSelected) {
            rows_selected = [];
        }
    })
    .catch(err => {

        console.error(err);
        alert("An error occurred during download.");
        hideOverlay();
        if (resetSelected) {
            rows_selected = [];
        }
    });
}


/**
 * It checks if the taxonomy is classified, and if it is, it calls the function to show the taxonomy
 * @param bench_id - the id of the bench
 * @returns The taxonomy of the sequence.
 */
function show_taxonomy(bench_id){
    if(document.getElementById("silva_taxon"+bench_id)){
        return;
    }
    if (document.getElementById("silva_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_silva(bench_id);
    }else{
        var el_silva = document.createElement("p");
        var nd_silva = document.createTextNode("Not Classified");
        el_silva.appendChild(nd_silva);
        el_silva.setAttribute("id", "silva_taxon"+bench_id)
        document.getElementById("silva_div"+bench_id).appendChild(el_silva);
    }
    if (document.getElementById("ena_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ena(bench_id);
    }else{
        var el_ena = document.createElement("p");
        var nd_ena = document.createTextNode("Not Classified");
        el_ena.appendChild(nd_ena);
        document.getElementById("ena_div"+bench_id).appendChild(el_ena);
    }
    if (document.getElementById("ltp_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ltp(bench_id);
    }else{
        var el_ltp = document.createElement("p");
        var nd_ltp = document.createTextNode("Not Classified");
        el_ltp.appendChild(nd_ltp);
        document.getElementById("ltp_div"+bench_id).appendChild(el_ltp);
    }
    if (document.getElementById("ncbi_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_ncbi(bench_id);
    }else{
        var el_ncbi = document.createElement("p");
        var nd_ncbi = document.createTextNode("Not Classified");
        el_ncbi.appendChild(nd_ncbi);
        document.getElementById("ncbi_div"+bench_id).appendChild(el_ncbi);
    }
    if (document.getElementById("gtdb_taxonomy" + bench_id).innerHTML.toString().split("'")[3] === 'Yes'){
        show_taxonomy_gtdb(bench_id);
    }else{
        var el_gtdb = document.createElement("p");
        var nd_gtdb = document.createTextNode("Not Classified");
        el_gtdb.appendChild(nd_gtdb);
        document.getElementById("gtdb_div"+bench_id).appendChild(el_gtdb);
    }
}


/**
 * Show silva taxonomy on search result table
 * @param bench_id
 */
function show_taxonomy_silva(bench_id) {
    var silva = document.getElementById('silva_taxonomy'+bench_id).innerHTML.toString();
    var temp = silva.split("'");
    var position = document.getElementById("silva_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "silva_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                console.log("Taxa:", temp[i])
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}


/**
 * Show ena taxonomy on search result table
 * @param bench_id
 */
function show_taxonomy_ena(bench_id) {
    var ena = document.getElementById('ena_taxonomy'+bench_id).innerHTML.toString();
    var temp = ena.split("'");
    var position = document.getElementById("ena_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "ena_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}


/**
 * Show gtdb taxonomy on search reasult table
 * @param bench_id
 */
function show_taxonomy_gtdb(bench_id) {
    var gtdb = document.getElementById('gtdb_taxonomy'+bench_id).innerHTML.toString();
    var temp = gtdb.split("'");
    var position = document.getElementById("gtdb_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "gtdb_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}


/**
 * Show ltp taxonomy on search result table
 * @param bench_id
 */
function show_taxonomy_ltp(bench_id) {
    var ltp = document.getElementById('ltp_taxonomy'+bench_id).innerHTML.toString();
    var temp = ltp.split("'");
    var position = document.getElementById("ltp_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "ltp_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}


/**
 * Show the ncbi taxonomy on search result table.
 * @param bench_id
 */
function show_taxonomy_ncbi(bench_id) {
    var ncbi = document.getElementById('ncbi_taxonomy'+bench_id).innerHTML.toString();
    var temp = ncbi.split("'");
    var position = document.getElementById("ncbi_div"+bench_id);
    var rank = []
    var rank_cont = 0
    for (var i = 5; i< temp.length;i++){
        if(i%2 !== 0){
            if(rank_cont%2 === 0){
                rank.push(temp[i])
            }else {
                var element = document.createElement("p");
                element.setAttribute("id", "ncbi_taxon" + bench_id);
                element.setAttribute("class", "popover-test")
                element.setAttribute("data-mdb-toggle", "popover")
                element.setAttribute("title", rank.pop())
                var node = document.createTextNode(temp[i]);
                element.appendChild(node);
                position.appendChild(element);
            }
            rank_cont++;
        }
    }
}

function showOverlay() {
    document.getElementById("loading_overlay").style.display = "flex";
}

function hideOverlay() {
    document.getElementById("loading_overlay").style.display = "none";
}

// acrivate autocomplet of organism names 
document.addEventListener('DOMContentLoaded', function() {
    setupAutocomplete(); // Avvia l'autocompletamento quando il DOM è pronto
});
