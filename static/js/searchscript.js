//searchCriteria è generato da Python nel file search_results.html
console.info(searchCriteria)
var rows_selected = [];
var table;

var lableCounter = document.getElementById("results-count");

window.showModal = function (data) { 
    // Rimuove eventuale modal precedente
    $('#dynamicModal').remove();
    const formatValue = (value) => {
        if (value === null || value === undefined || value === '') return '--';
        if (typeof value === 'boolean') return value ? 'Yes' : 'No';
        return value;
    };
    const taxonomyHtml = (data.taxonomy || []).map(tax => {
        const standardRanks = [
            'domain',
            'superkingdom',
            'phylum',
            'class',
            'order',
            'family',
            'genus',
            'species'
        ];
        const ranksHtml = standardRanks
            .filter(rank => tax[rank] !== undefined)
            .map(rank => `
                <div>
                    <strong>${rank.charAt(0).toUpperCase() + rank.slice(1)}:</strong>
                    ${formatValue(tax[rank])}
                </div>
            `)
            .join('');
        const extraRanksHtml = tax.extra_ranks
            ? `
                <div style="margin-top:8px">
                    <strong>Extra ranks</strong>
                    <ul style="margin-bottom:0">
                        ${Object.entries(tax.extra_ranks)
                .map(([k, v]) => `<li><strong>${k}:</strong> ${v}</li>`)
                .join('')}
                    </ul>
                </div>
            `
            : '';
        return `
            <div class="taxa_div mb-3">
                <h6>${tax.source}</h6>
                <div>
                    <strong>Classified:</strong>
                    ${formatValue(tax.is_classified)}
                </div>
                ${ranksHtml}
                ${extraRanksHtml}
                <hr>
            </div>
        `;
    }).join('');
    const modalHtml = `
        <div class="modal fade"
             id="dynamicModal"
             tabindex="-1"
             aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            ${formatValue(data.organism_name)}
                        </h5>
                        
                    </div>
                    <div class="modal-body">
                        <p><strong>Organism Name:</strong> ${formatValue(data.organism_name)}</p>
                        <p><strong>Accession Number:</strong> ${formatValue(data.accession_number)}</p>
                        <p><strong>Reference Id:</strong> ${formatValue(data.reference_id)}</p>
                        <p><strong>Length:</strong> ${formatValue(data.length)}</p>
                        <p><strong>Unpaired Bases:</strong> ${formatValue(data.num_unpaired_bases)}</p>
                        <p><strong>Base Pairs:</strong> ${formatValue(data.num_base_pairs)}</p>
                        <p><strong>Pseudoknotted:</strong> ${formatValue(data.is_pseudoknotted)}</p>
                        <p><strong>Pseudoknot Order:</strong> ${formatValue(data.pseudoknot_order)}</p>
                        <p><strong>RNA Type:</strong> ${formatValue(data.rna_type)}</p>
                        <p><strong>Genus:</strong> ${formatValue(data.genus)}</p>
                        <p>
                            <strong>Core:</strong><br>
                            <small style="word-break: break-all;">
                                ${formatValue(data.core)}
                            </small>
                        </p>
                        <p>
                            <strong>Core Plus:</strong><br>
                            <small style="word-break: break-all;">
                                ${formatValue(data.core_plus)}
                            </small>
                        </p>
                        <p>
                            <strong>Shape:</strong><br>
                            <small style="word-break: break-all;">
                                ${formatValue(data.shape)}
                            </small>
                        </p>
                        <p><strong>Database:</strong> ${formatValue(data.database)}</p>
                        <p><strong>Reference:</strong> ${formatValue(data.reference)}</p>
                        <p><strong>Description:</strong> ${formatValue(data.description)}</p>
                        <hr>
                        <h4>Taxonomies</h4>
                        ${taxonomyHtml || '<p>--</p>'}
                    </div>
                    <div class="modal-footer">
                        <button type="button"
                                class="btn btn-secondary"
                                data-dismiss="modal">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    $('body').append(modalHtml);

    const modal = new bootstrap.Modal(

        document.getElementById('dynamicModal')

    );
    modal.show();
    $('#dynamicModal').on('hidden.bs.modal', function () {
        $(this).remove();
    });

};

$(document).ready(function () {
    table = $('#result_table').DataTable({
        processing: true,
        serverSide: true,
        paging: true,

        ajax: function (data, callback) {

            $.ajax({
                url: '/phylorna/search/res/?format=json',
                type: 'POST',
                data: {
                    ...searchCriteria,
                    offset: data.start,
                    limit: data.length
                },
                success: function (resp) {

                    callback({
                        draw: data.draw,
                        recordsTotal: resp.total,
                        recordsFiltered: resp.total,
                        data: resp.results
                    });
                    lableCounter.innerText = resp.total + " results";
                }
            });
        },

        rowId: '_id',

        columns: [
            {
                data: null,
                orderable: false,
                searchable: false,
                render: function (data) {
                    return `<input type="checkbox" class="row-check" id="${data.reference_id}">`;
                }
            },
            { data: 'organism_name' },
            { data: 'reference_id' },
            { data: 'accession_number' },
            { data: 'rna_type' },
            {
                data: null,
                orderable: false,
                searchable: false,
                render: function (data) {
                    return `<button type="button" id="btn-moreInformation" onclick='showModal(${JSON.stringify(data)})'>...</button>`;
                }
            }
        ]
    });
    $('#check_all').on('click', function () {
        var rows = table.rows({ 'page': 'current' }).nodes(); // Solo righe visibili
        $('input[type="checkbox"]', rows).prop('checked', this.checked);
    });
    $('#result_table tbody').on('change', 'input[type="checkbox"]', function () {
        if (!this.checked) {
            var el = $('#check_all').get(0);
            if (el && el.checked && ('indeterminate' in el)) {
                el.indeterminate = true;
            }
        }
    });
    $('#check_all').on('click', function (e) {
        var rows = table.rows({ 'page': 'current' }).nodes(); // Solo righe visibili nella pagina
        var checked = this.checked;

        // Seleziona/Deseleziona le checkbox nella pagina visibile
        $('input[type="checkbox"]', rows).prop('checked', checked);

        // Aggiorna l'array rows_selected solo con gli elementi della pagina visibile
        if (checked) {
            $('input[type="checkbox"]:checked', rows).each(function () {
                var ref_id = $(this).attr('id');
                if (!rows_selected.includes(ref_id)) {
                    rows_selected.push(ref_id);
                }
            });
        } else {
            $('input[type="checkbox"]', rows).each(function () {
                var ref_id = $(this).attr('id');
                rows_selected = rows_selected.filter(id => id !== ref_id); // Rimuove i deselezionati
            });
        }
        console.log("Righe selezionate nella pagina attuale:", rows_selected); // DEBUG
    });
    $('#result_table tbody').on('click', 'input[type="checkbox"]', function (e) {
        var $row = $(this).closest('tr');
        var data = table.row($row).data();
        var ref_id = data.reference_id;
        console.log(data);
        if (this.checked) {
            $row.addClass('selected');
            rows_selected[cont] = ref_id;
            console.log("cont: " + cont)
            cont++;
        } else {
            $row.removeClass('selected');
            rows_selected[rows_selected.indexOf(ref_id)] = '';
        }
        e.stopPropagation();
        var node = document.createTextNode(rows_selected);
        var element = document.getElementById("hidden_ref_array");
        element.appendChild(node);
    });
});
function download_all() {
    console.info("Download all");
    console.info(searchCriteria);

    $.ajax({
        url: '/phylorna/search/names/',
        type: 'POST',
        data: searchCriteria, // oggetto JavaScript
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        dataType: 'json'
    }).done(function (data, textStatus, xhr) {
        console.log(data.results); // Stampa il JSON restituito dal server
        rows_selected = data.results;
        final_download();
    }).fail(function (xhr, status, error) {
        console.error(error);
    });
}
var rows_selected = [];
cont = 0;
$(document).ready(function () {
})